from fastapi import HTTPException, Depends, APIRouter
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from .models import Product
from database import get_db
from .schemas import ProductResponse, ProductCreate, ProductUpdate

app = APIRouter()


@app.get("/", response_model=List[ProductResponse])
async def get_products(db: AsyncSession = Depends(get_db), category: Optional[str] = None):
    query = select(Product)
    if category:
        query = query.filter(Product.category == category)
    result = await db.execute(query)
    products = result.scalars().all()
    if not products:
        raise HTTPException(status_code=404, detail="Product not found")
    return products


@app.post("/", response_model=ProductResponse)
async def create_product(product: ProductCreate, db: AsyncSession = Depends(get_db)):
    new_product = Product(**product.model_dump())
    db.add(new_product)
    try:
        await db.commit()
        await db.refresh(new_product)
        return new_product
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Product creation failed")


@app.patch("/{id}", response_model=ProductResponse)
async def update_product(id: int, product: ProductUpdate, db: AsyncSession = Depends(get_db)):
    query = select(Product).filter(Product.id == id)
    result = await db.execute(query)
    print(result.__dict__)
    existing_product = result.scalars().first()
    if not existing_product:
        raise HTTPException(status_code=404, detail="Product not found")
    for key, value in product.model_dump(exclude_unset=True).items():
        print(key)
        setattr(existing_product, key, value)
    db.add(existing_product)
    await db.commit()
    await db.refresh(existing_product)
    return existing_product
