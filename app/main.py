from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from pwdlib import PasswordHash
from app.db import models
from app.db.database import Base, engine, get_db
from app.schemas.user import UserCreate, UserResponse


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="FinFlow API",
    version="0.1.0",
)


password_hash = PasswordHash.recommended()

@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post(
    "/users",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db),
):
    existing_user = db.scalar(
        select(models.User).where(
            (models.User.username == user.username)
            | (models.User.email == user.email)
        )
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username or email already exists",
        )

    hashed_password = password_hash.hash(user.password)

    new_user = models.User(
        username=user.username,
        email=user.email,
        password_hash=hashed_password,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user