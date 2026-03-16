from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.model import CartItemCreate, CartItemUpdate, CartResponse
from app.db.database import get_db
from app.dependencies.decodingtokens import get_current_user
from app.dependencies.auth_context import AuthContext

from app.services import cart_service


router = APIRouter(
    prefix="/cart",
    tags=["Cart"]
)


# Add item to cart
@router.post("/add")
def add_to_cart(
    item: CartItemCreate,
    current_user: AuthContext = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    result = cart_service.add_to_cart(
        user_id=current_user.user.user_id,
        product_id=item.product_id,
        quantity=item.quantity,
        db=db
    )

    if result is None:
        raise HTTPException(status_code=404, detail="Product not found")

    return {"message": "Item added to cart"}
    

# Update quantity
@router.patch("/update/{product_id}")
def update_cart_item(
    product_id: int,
    item: CartItemUpdate,
    current_user: AuthContext = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    result = cart_service.update_cart_item(
        user_id=current_user.user.user_id,
        product_id=product_id,
        quantity=item.quantity,
        db=db
    )

    if result is None:
        raise HTTPException(status_code=404, detail="Cart item not found")

    return {"message": "Cart item updated"}


# Remove item from cart
@router.delete("/remove/{product_id}")
def remove_cart_item(
    product_id: int,
    current_user: AuthContext = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    deleted = cart_service.remove_cart_item(
        user_id=current_user.user.user_id,
        product_id=product_id,
        db=db
    )

    if not deleted:
        raise HTTPException(status_code=404, detail="Cart item not found")

    return {"message": "Item removed from cart"}


# Get full cart
@router.get("/", response_model=CartResponse)
def get_user_cart(
    current_user: AuthContext = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    return cart_service.get_user_cart(
        user_id=current_user.user.user_id,
        db=db
    )