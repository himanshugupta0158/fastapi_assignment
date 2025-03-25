from pydantic import BaseModel, validator


class ProductBase(BaseModel):
    name: str
    description: str | None = None
    price: float
    stock: int


class ProductCreate(ProductBase):
    @validator("price")
    def price_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("Price must be a positive number")
        return v

    @validator("stock")
    def stock_must_be_non_negative(cls, v):
        if v < 0:
            raise ValueError("Stock cannot be negative")
        return v


class ProductUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    stock: int | None = None

    @validator("price", pre=True, always=True)
    def price_must_be_positive(cls, v):
        if v is not None and v <= 0:
            raise ValueError("Price must be a positive number")
        return v

    @validator("stock", pre=True, always=True)
    def stock_must_be_non_negative(cls, v):
        if v is not None and v < 0:
            raise ValueError("Stock cannot be negative")
        return v


class Product(ProductBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
