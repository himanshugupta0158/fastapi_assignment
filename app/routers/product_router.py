from typing import List

from fastapi import APIRouter, Depends, HTTPException

from app.dependencies import get_current_user
from app.models.user import User
from app.repositories.product_repository import (
    ProductRepository,
    get_product_repository,
)
from app.schemas.product import Product, ProductCreate, ProductUpdate

router = APIRouter(tags=["products"])


@router.post("", response_model=Product)
def create_product(
    product: ProductCreate,
    product_repo: ProductRepository = Depends(get_product_repository),
    current_user: User = Depends(get_current_user),
):
    try:
        return product_repo.create_product(product, user_id=current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{product_id}", response_model=Product)
def get_product(
    product_id: int, product_repo: ProductRepository = Depends(get_product_repository)
):
    product = product_repo.get_product(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.get("", response_model=List[Product])
def get_all_products(product_repo: ProductRepository = Depends(get_product_repository)):
    return product_repo.get_all_products()


@router.put("/{product_id}", response_model=Product)
def update_product(
    product_id: int,
    product_update: ProductUpdate,
    product_repo: ProductRepository = Depends(get_product_repository),
    current_user: User = Depends(get_current_user),
):
    try:
        return product_repo.update_product(product_id, current_user.id, product_update)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{product_id}")
def delete_product(
    product_id: int,
    product_repo: ProductRepository = Depends(get_product_repository),
    current_user: User = Depends(get_current_user),
):
    try:
        product_repo.delete_product(product_id, current_user.id)
        return {"message": "Product deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
