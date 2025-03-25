from typing import List

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate


class ProductRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_product(self, product: ProductCreate, user_id: int) -> Product:
        db_product = Product(**product.model_dump(), user_id=user_id)  # Add user_id
        self.db.add(db_product)
        self.db.commit()
        self.db.refresh(db_product)
        return db_product

    def get_product(self, product_id: int) -> Product | None:
        return self.db.query(Product).filter(Product.id == product_id).first()

    def get_all_products(self) -> List[Product]:
        return self.db.query(Product).all()

    def update_product(
        self, product_id: int, user_id: int, product_update: ProductUpdate
    ) -> Product:
        db_product = self.get_product(product_id)
        if not db_product:
            raise HTTPException(status_code=404, detail="Product does not exist")

        if db_product.user_id != user_id:
            raise HTTPException(
                status_code=400, detail="You are not allowed to update this product."
            )

        update_data = product_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_product, key, value)

        self.db.commit()
        self.db.refresh(db_product)
        return db_product

    def delete_product(self, product_id: int, user_id: int) -> None:
        db_product = self.get_product(product_id)
        if not db_product:
            raise HTTPException(status_code=404, detail="Product does not exist")

        if db_product.user_id != user_id:
            raise HTTPException(
                status_code=400, detail="You are not allowed to delete this product."
            )

        self.db.delete(db_product)
        self.db.commit()


def get_product_repository(db: Session = Depends(get_db)):
    return ProductRepository(db=db)
