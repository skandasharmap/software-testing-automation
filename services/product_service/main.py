
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import Float, Integer, String, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

app = FastAPI(title="Product Service", version="1.0")

engine = create_engine(
    "sqlite:///product.db",
    connect_args={"check_same_thread": False},
)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    pass


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    stock: Mapped[int] = mapped_column(Integer, nullable=False, default=0)


Base.metadata.create_all(engine)


class ProductIn(BaseModel):
    name: str = Field(..., min_length=2)
    price: float = Field(..., ge=0.0)
    stock: int = Field(0, ge=0)


class ProductOut(ProductIn):
    id: int


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/products", response_model=ProductOut, status_code=201)
def create_product(p: ProductIn):
    with SessionLocal() as db:
        prod = Product(name=p.name, price=p.price, stock=p.stock)
        db.add(prod)
        db.commit()
        db.refresh(prod)

        return ProductOut(
            id=prod.id,
            name=prod.name,
            price=prod.price,
            stock=prod.stock,
        )


@app.get("/products/{pid}", response_model=ProductOut)
def get_product(pid: int):
    with SessionLocal() as db:
        prod = db.get(Product, pid)
        if not prod:
            raise HTTPException(status_code=404, detail="Not found")

        return ProductOut(
            id=prod.id,
            name=prod.name,
            price=prod.price,
            stock=prod.stock,
        )


@app.put("/products/{pid}", response_model=ProductOut)
def update_product(pid: int, p: ProductIn):
    with SessionLocal() as db:
        prod = db.get(Product, pid)
        if not prod:
            raise HTTPException(status_code=404, detail="Not found")

        prod.name = p.name
        prod.price = p.price
        prod.stock = p.stock

        db.commit()
        db.refresh(prod)

        return ProductOut(
            id=prod.id,
            name=prod.name,
            price=prod.price,
            stock=prod.stock,
        )


@app.post("/products/{pid}/reserve", response_model=ProductOut)
def reserve_stock(pid: int, qty: int = 1):
    if qty <= 0:
        raise HTTPException(status_code=400, detail="qty must be > 0")

    with SessionLocal() as db:
        prod = db.get(Product, pid)
        if not prod:
            raise HTTPException(status_code=404, detail="Not found")
        if prod.stock < qty:
            raise HTTPException(status_code=409, detail="Insufficient stock")

        prod.stock -= qty
        db.commit()
        db.refresh(prod)

        return ProductOut(
            id=prod.id,
            name=prod.name,
            price=prod.price,
            stock=prod.stock,
        )


@app.post("/products/{pid}/release", response_model=ProductOut)
def release_stock(pid: int, qty: int = 1):
    if qty <= 0:
        raise HTTPException(status_code=400, detail="qty must be > 0")

    with SessionLocal() as db:
        prod = db.get(Product, pid)
        if not prod:
            raise HTTPException(status_code=404, detail="Not found")

        prod.stock += qty
        db.commit()
        db.refresh(prod)

        return ProductOut(
            id=prod.id,
            name=prod.name,
            price=prod.price,
            stock=prod.stock,
        )
