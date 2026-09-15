from fastapi import FastAPI

from app.api.auth import router as auth_router
from app.api.users import router as users_router
from app.db import models
from app.db.database import Base, engine


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="FinFlow API",
    version="0.1.0",
)


app.include_router(users_router)
app.include_router(auth_router)


@app.get("/health")
def health_check():
    return {"status": "ok"}