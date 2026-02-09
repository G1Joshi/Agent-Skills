---
name: fastapi
description: FastAPI Python async framework with Pydantic and automatic OpenAPI. Use for Python APIs.
---

# FastAPI

Modern Python async web framework with automatic API documentation.

## When to Use

- Building REST APIs
- High-performance async services
- APIs with automatic documentation
- Microservices with Python

## Quick Start

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    name: str
    email: str

@app.get("/users/{user_id}")
async def get_user(user_id: int) -> User:
    return await db.get_user(user_id)

@app.post("/users", status_code=201)
async def create_user(user: User) -> User:
    return await db.create_user(user)
```

## Core Concepts

### Pydantic Models

```python
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime

class UserBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True  # For ORM mode
```

### Dependency Injection

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

oauth2 = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: str = Depends(oauth2)) -> User:
    user = await verify_token(token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/me")
async def get_me(user: User = Depends(get_current_user)) -> UserResponse:
    return user
```

## Common Patterns

### Router Organization

```python
# routers/users.py
from fastapi import APIRouter, Depends

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/")
async def list_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
) -> list[UserResponse]:
    return await crud.get_users(db, skip=skip, limit=limit)

# main.py
from routers import users, posts
app.include_router(users.router)
app.include_router(posts.router)
```

### Error Handling

```python
from fastapi import HTTPException
from fastapi.responses import JSONResponse

class NotFoundError(Exception):
    def __init__(self, resource: str):
        self.resource = resource

@app.exception_handler(NotFoundError)
async def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"detail": f"{exc.resource} not found"}
    )
```

## Best Practices

**Do**:

- Use Pydantic for validation
- Use dependency injection
- Use async for I/O operations
- Organize with routers

**Don't**:

- Block the event loop
- Skip input validation
- Return ORM models directly
- Ignore error handling

## Troubleshooting

| Issue                | Cause           | Solution             |
| -------------------- | --------------- | -------------------- |
| 422 Validation Error | Schema mismatch | Check Pydantic model |
| Slow response        | Blocking I/O    | Use async operations |
| Circular import      | Router imports  | Use late binding     |

## References

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
