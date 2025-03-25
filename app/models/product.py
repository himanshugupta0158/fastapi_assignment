from sqlalchemy import Float, ForeignKey, Integer, String
from sqlalchemy.orm import mapped_column, relationship

from app.database import Base


class Product(Base):
    __tablename__ = "products"

    id = mapped_column(Integer, primary_key=True, index=True)
    name = mapped_column(String, index=True, nullable=False)
    description = mapped_column(String, nullable=True)
    price = mapped_column(Float, nullable=False)
    stock = mapped_column(Integer, nullable=False)
    user_id = mapped_column(Integer, ForeignKey("users.id"), nullable=False)

    user = relationship("User", back_populates="products")
