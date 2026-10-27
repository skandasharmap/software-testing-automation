import hashlib
from datetime import datetime, timedelta

from fastapi import Depends, FastAPI, HTTPException
from jose import JWTError, jwt
from pydantic import BaseModel, Field
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

SECRET = "change-me-in-prod"
ALGO = "HS256"

app = FastAPI(title="Auth Service", version="1.0")

engine = create_engine("sqlite:///auth.db", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    pwd_hash = Column(String, nullable=False)


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


def hash_pwd(p: str) -> str:
    return hashlib.sha256(p.encode()).hexdigest()


def create_token(sub: str) -> str:
    exp = datetime.utcnow() + timedelta(hours=2)
    payload = {"sub": sub, "exp": exp}
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
        raise HTTPException(status_code=401, detail="Invalid token")
    user = db.query(User).filter_by(email=sub).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user


@app.post("/register", response_model=TokenOut, status_code=201)
def register(inp: RegisterIn, db: Session = Depends(get_db)):
    if db.query(User).filter_by(email=inp.email).first():
        raise HTTPException(400, "User exists")
    u = User(email=inp.email, name=inp.name, pwd_hash=hash_pwd(inp.password))
    db.add(u)
    db.commit()
    return TokenOut(access_token=create_token(u.email))


@app.post("/login", response_model=TokenOut)
def login(inp: LoginIn, db: Session = Depends(get_db)):
    u = db.query(User).filter_by(email=inp.email).first()
    if not u or u.pwd_hash != hash_pwd(inp.password):
        raise HTTPException(401, "Invalid credentials")
    return TokenOut(access_token=create_token(u.email))


@app.get("/me")
def me(authorization: str, db: Session = Depends(get_db)):
    if not authorization.lower().startswith("bearer "):
        raise HTTPException(401, "Missing bearer")
    token = authorization.split(" ", 1)[1]
    u = get_current_user(token, db)
    return {"email": u.email, "name": u.name, "id": u.id}
