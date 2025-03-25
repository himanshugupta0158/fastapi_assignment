from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import create_access_token, verify_password
from app.models.user import User
from app.schemas.auth import LoginRequest


class AuthRepository:
    def __init__(self, db: Session):
        self.db = db

    def user_login(self, creds: LoginRequest):
        user = (
            self.db.query(User)
            .filter(
                (User.username == creds.username_or_email)
                | (User.email == creds.username_or_email)
            )
            .first()
        )
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User with such credentials not found!",
            )

        if not verify_password(creds.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Password"
            )

        user.version += 1
        token = create_access_token({"user_id": user.id, "version": user.version})
        self.db.commit()
        return {"user_id": user.id, "access_token": token}

    def user_logout(self, user: User):
        user.version += 1
        self.db.commit()
        return {"message": "Successfully logged out"}


def get_auth_repository(db: Session = Depends(get_db)):
    return AuthRepository(db=db)
