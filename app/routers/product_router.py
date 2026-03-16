from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from app.schemas.model import ProductCreate, ProductUpdate, ProductResponse
from app.db.database import get_db
from app.dependencies.permissions import require_role
from app.dependencies.auth_context import AuthContext

from app.services import product_service


router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


@router.get("/", response_model=List[ProductResponse])
def get_products(db: Session = Depends(get_db)):
    return product_service.get_all_products(db)


@router.get("/{id}", response_model=ProductResponse)
def get_product(id: int, db: Session = Depends(get_db)):

    product = product_service.get_product_by_id(id, db)

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return product


@router.post("/", response_model=ProductResponse)
def create_product(
    product: ProductCreate,
    current_user: AuthContext = Depends(require_role("admin")),
    db: Session = Depends(get_db)
):

    return product_service.create_product(product, db)


@router.put("/{id}", response_model=ProductResponse)
def replace_product(
    id: int,
    product: ProductCreate,
    current_user: AuthContext = Depends(require_role("admin")),
    db: Session = Depends(get_db)
):

    updated = product_service.replace_product(id, product, db)

    if not updated:
        raise HTTPException(status_code=404, detail="Product not found")

    return updated


@router.patch("/{id}", response_model=ProductResponse)
def update_product(
    id: int,
    product_update: ProductUpdate,
    current_user: AuthContext = Depends(require_role("admin")),
    db: Session = Depends(get_db)
):

    updated = product_service.update_product(id, product_update, db)

    if not updated:
        raise HTTPException(status_code=404, detail="Product not found")

    return updated


@router.delete("/{id}", status_code=204)
def delete_product(
    id: int,
    current_user: AuthContext = Depends(require_role("admin")),
    db: Session = Depends(get_db)
):

    deleted = product_service.delete_product(id, db)

    if not deleted:
        raise HTTPException(status_code=404, detail="Product not found")