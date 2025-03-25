from fastapi import FastAPI

from app.database import Base, engine
from app.models import Product, User
from app.routers import auth_router, product_router, user_router

app = FastAPI(
    title="FastAPI Assignment API",
    description=(
        "This API is part of a FastAPI assignment project. It provides endpoints for user authentication, "
        "money transfers between users, and product management. Key features include:\n"
        "- JWT-based authentication with login and logout functionality.\n"
        "- User management (register, fetch users, check balances).\n"
        "- Product management (create, update, delete, fetch products).\n"
        "- Money transfer between users with transaction rollback on failure.\n"
        "The API uses SQLite as the database for simplicity, but it can be extended to use other databases like PostgreSQL."
    ),
    version="1.0.0",
)


Base.metadata.create_all(bind=engine)


app.include_router(auth_router.router, prefix="/auth")
app.include_router(product_router.router, prefix="/product")
app.include_router(user_router.router, prefix="/user")


@app.get("/health")
def health_check():
    return {"message": "Ok"}
