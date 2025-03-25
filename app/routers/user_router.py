from typing import List

from fastapi import APIRouter, Depends, HTTPException

from app.dependencies import get_current_user
from app.repositories.user_repository import UserRepository, get_user_repository
from app.schemas.user import User, UserCreate

router = APIRouter(tags=["users"])


@router.get("/balance")
def get_user_balance(
    user_repo: UserRepository = Depends(get_user_repository),
    current_user: User = Depends(get_current_user),
):
    try:
        balance = user_repo.get_user_balance(current_user.id)
        return {"user_id": current_user.id, "balance": balance}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/transfer")
def transfer_money(
    sender_id: int,
    receiver_id: int,
    amount: float,
    user_repo: UserRepository = Depends(get_user_repository),
    current_user: User = Depends(get_current_user),
):
    try:
        user_repo.transfer_money(sender_id, receiver_id, amount)
        return {"message": "Transfer successful"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/recharge_balance")
def recharge(
    amount: float,
    user_repo: UserRepository = Depends(get_user_repository),
    current_user: User = Depends(get_current_user),
):
    try:
        user = user_repo.recharge(amount, current_user)
        return {"message": "Recharge successful", "amount": user.balance}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/register", response_model=User)
def register_user(
    user: UserCreate, user_repo: UserRepository = Depends(get_user_repository)
):
    existing_user = user_repo.get_user_by_username(user.username)
    if existing_user:
        raise HTTPException(
            status_code=400, detail="User with this username already exists"
        )
    existing_email = user_repo.get_user_by_email(user.email)
    if existing_email:
        raise HTTPException(
            status_code=400, detail="User with this email already exists"
        )
    return user_repo.create_user(user)


@router.get("/{user_id}", response_model=User)
def get_user(
    user_id: int,
    user_repo: UserRepository = Depends(get_user_repository),
    current_user: User = Depends(get_current_user),
):
    user = user_repo.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/", response_model=List[User])
def get_all_users(
    user_repo: UserRepository = Depends(get_user_repository),
    current_user: User = Depends(get_current_user),
):
    return user_repo.get_all_users()
