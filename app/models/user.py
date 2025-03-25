from sqlalchemy import Float, Integer, String
from sqlalchemy.orm import mapped_column, relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"
    id = mapped_column(Integer, primary_key=True, autoincrement=True, index=True)
    username = mapped_column(String, unique=True, nullable=False)
    email = mapped_column(String, unique=True, nullable=False)
    password = mapped_column(String, nullable=False)
    version = mapped_column(Integer, default=0, nullable=False)
    balance = mapped_column(Float, default=0.0, nullable=False)

    products = relationship("Product", back_populates="user")
