from typing import List

from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_password_hash
from app.models.user import User
from app.schemas.user import UserCreate


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_username(self, username: str) -> User | None:
        return self.db.query(User).filter(User.username == username).first()

    def get_user_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(User.email == email).first()

    def get_user(self, user_id: int) -> User | None:
        return self.db.query(User).filter(User.id == user_id).first()

    def get_all_users(self) -> List[User]:
        return self.db.query(User).all()

    def get_user_balance(self, user_id: int) -> float:
        user = self.get_user(user_id)
        if not user:
            raise ValueError("User does not exist")
        return user.balance

    def create_user(self, user: UserCreate) -> User:
        hashed_password = get_password_hash(user.password)  # Hash the password
        db_user = User(
            username=user.username,  # Changed from name to username
            email=user.email,  # Added email
            password=hashed_password,
            balance=0.0,
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def transfer_money(self, sender_id: int, receiver_id: int, amount: float) -> None:
        sender = self.get_user(sender_id)
        receiver = self.get_user(receiver_id)

        if not sender or not receiver:
            raise ValueError("Sender or receiver does not exist")

        if sender.balance < amount:
            raise ValueError("Insufficient balance in sender's account")

        try:
            sender.balance -= amount
            receiver.balance += amount
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise e

    def recharge(self, amount, current_user: User):
        current_user.balance += amount
        self.db.commit()
        return current_user


def get_user_repository(db: Session = Depends(get_db)):
    return UserRepository(db=db)
