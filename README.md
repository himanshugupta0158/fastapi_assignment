# FastAPI Assignment API

![FastAPI](https://img.shields.io/badge/FastAPI-0.68.0-green.svg)
![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![SQLite](https://img.shields.io/badge/Database-SQLite-lightgrey.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## Overview

This project is a **FastAPI-based REST API** developed as part of an assignment. It provides endpoints for user authentication, money transfers between users, and product management. The API uses **JWT-based authentication** for secure access, **SQLite** as the database (with the option to extend to other databases like PostgreSQL), and follows a clean architecture with dependency injection and repository patterns.

### Key Features
- **User Authentication**: Register, login, and logout with JWT tokens.
- **User Management**: Register users, fetch user details, check balances, and recharge accounts.
- **Product Management**: Create, update, delete, and fetch products (with user ownership).
- **Money Transfers**: Transfer money between users with transaction rollback on failure.
- **Security**: JWT token validation, token versioning for logout, and user-specific access control for product operations.

## Project Structure
```
fastapi-assignment/
│
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app initialization and router setup
│   ├── database.py             # Database setup (SQLite with SQLAlchemy)
│   ├── models/                 # SQLAlchemy models
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── product.py
│   ├── schemas/                # Pydantic schemas for request/response validation
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── user.py
│   │   └── product.py
│   ├── repositories/           # Repository layer for database operations
│   │   ├── __init__.py
│   │   ├── auth_repository.py
│   │   ├── user_repository.py
│   │   └── product_repository.py
│   ├── routers/                # API route definitions
│   │   ├── __init__.py
│   │   ├── auth_router.py
│   │   ├── user_router.py
│   │   └── product_router.py
│   └── utils/
│       ├── __init__.py
│       └── dependencies.py     # Authentication utilities (JWT, password hashing)
│
├── requirements.txt            # Project dependencies
└── README.md                   # Project documentation
```


## Prerequisites

- **Python 3.9+**
- **pip** (Python package manager)
- **Virtualenv** (recommended for isolated environments)

## Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/fastapi-assignment.git
   cd fastapi-assignment
   ```
2. **Create a Virtual Environment**
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. **Install Dependencies**
    ```
    pip install -r requirements.txt
    ```

4. **Run FastAPI Project**
    ```
    fastapi dev main.py # if you are inside app folder
    ```
    or
    ```
    fastapi dev app/main.py # if you are outside app folder
    ```
5. **Access API Documentation**
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc