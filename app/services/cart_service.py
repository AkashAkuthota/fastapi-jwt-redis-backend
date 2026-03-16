from sqlalchemy.orm import Session
import app.db.database_models as database_models

import logging

logger = logging.getLogger(__name__)


def add_to_cart(user_id: int, product_id: int, quantity: int, db: Session):

    product = db.query(database_models.Product).filter(
        database_models.Product.id == product_id
    ).first()

    if not product:
        logger.warning(f"Product {product_id} not found")
        return None

    cart_item = db.query(database_models.CartItem).filter(
        database_models.CartItem.user_id == user_id,
        database_models.CartItem.product_id == product_id
    ).first()

    if cart_item:
        cart_item.quantity += quantity
        logger.info(f"Updated cart item quantity for user {user_id}, product {product_id}")
    else:
        cart_item = database_models.CartItem(
            user_id=user_id,
            product_id=product_id,
            quantity=quantity
        )
        db.add(cart_item)
        logger.info(f"Added new cart item for user {user_id}, product {product_id}")

    db.commit()
    db.refresh(cart_item)

    return cart_item


def update_cart_item(user_id: int, product_id: int, quantity: int, db: Session):

    cart_item = db.query(database_models.CartItem).filter(
        database_models.CartItem.user_id == user_id,
        database_models.CartItem.product_id == product_id
    ).first()

    if not cart_item:
        logger.warning(f"Product {product_id} not found")
        return None

    cart_item.quantity = quantity

    db.commit()
    db.refresh(cart_item)

    return cart_item


def remove_cart_item(user_id: int, product_id: int, db: Session):

    cart_item = db.query(database_models.CartItem).filter(
        database_models.CartItem.user_id == user_id,
        database_models.CartItem.product_id == product_id
    ).first()

    if not cart_item:
        logger.warning(f"Product {product_id} not found")
        return False

    db.delete(cart_item)
    db.commit()

    return True



def get_user_cart(user_id: int, db: Session):

    results = (
        db.query(
            database_models.Product.id,
            database_models.Product.name,
            database_models.Product.price,
            database_models.Product.quantity,
            database_models.CartItem.quantity
        )
        .join(
            database_models.CartItem,
            database_models.Product.id == database_models.CartItem.product_id
        )
        .filter(database_models.CartItem.user_id == user_id)
        .all()
    )

    items = []
    cart_total = 0

    for product_id, name, price,stock_quantity, cart_quantity in results:

        total_price = price * cart_quantity
        cart_total += total_price

        items.append({
            "product_id": product_id,
            "product_name": name,
            "price": price,
            "quantity": cart_quantity,
            "total_price": total_price,
            "in_stock": stock_quantity > 0
        })

    return {
        "items": items,
        "cart_total": cart_total
    }