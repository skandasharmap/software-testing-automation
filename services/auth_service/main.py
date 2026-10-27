
import hashlib
import os
from datetime import datetime, timedelta, timezone

from fastapi import Depends, FastAPI, Header, HTTPException
from jose import JWTError, jwt
from pydantic import BaseModel, Field
from sqlalchemy import Integer, String, create_engine
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    Session,
    mapped_column,
    sessionmaker,
)

SECRET = os.getenv("JWT_SECRET", "change-me-in-prod")
ALGO = "HS256"

app = FastAPI(title="Auth Service", version="1.0")

engine = create_engine(
    "sqlite:///auth.db",
    connect_args={"check_same_thread": False},
)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )
    email: Mapped[str] = mapped_column(
        String,
        unique=True,
        index=True,
        nullable=False,
    )
    name: Mapped[str] = mapped_column(String, nullable=False)
    pwd_hash: Mapped[str] = mapped_column(String, nullable=False)


Base.metadata.create_all(engine)


class RegisterIn(BaseModel):
    email: str = Field(..., examples=["test@example.com"])
    name: str
    password: str = Field(..., min_length=6)


class LoginIn(BaseModel):
    email: str
    password: str


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"


def hash_pwd(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def create_token(sub: str) -> str:
    expiration = datetime.now(timezone.utc) + timedelta(hours=2)
    payload = {"sub": sub, "exp": expiration}
    return jwt.encode(payload, SECRET, algorithm=ALGO)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(token: str, db: Session) -> User:
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGO])
        sub = payload.get("sub")
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token",
        )

    if not sub:
        raise HTTPException(
            status_code=401,
            detail="Invalid token subject",
        )

    user = db.query(User).filter_by(email=sub).first()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="User not found",
        )

    return user


@app.post("/register", response_model=TokenOut, status_code=201)
def register(
    inp: RegisterIn,
    db: Session = Depends(get_db),
):
    existing_user = db.query(User).filter_by(email=inp.email).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="User exists",
        )

    user = User(
        email=inp.email,
        name=inp.name,
        pwd_hash=hash_pwd(inp.password),
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return TokenOut(access_token=create_token(user.email))


@app.post("/login", response_model=TokenOut)
def login(
    inp: LoginIn,
    db: Session = Depends(get_db),
):
    user = db.query(User).filter_by(email=inp.email).first()

    if not user or user.pwd_hash != hash_pwd(inp.password):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials",
        )

    return TokenOut(access_token=create_token(user.email))


@app.get("/me")
def me(
    authorization: str | None = Header(default=None),
    db: Session = Depends(get_db),
):
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(
            status_code=401,
            detail="Missing bearer",
        )

    token = authorization.split(" ", 1)[1].strip()

    if not token:
        raise HTTPException(
            status_code=401,
            detail="Missing bearer token",
        )

    user = get_current_user(token, db)

    return {
        "email": user.email,
        "name": user.name,
        "id": user.id,
    }
