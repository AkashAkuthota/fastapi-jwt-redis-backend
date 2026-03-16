from sqlalchemy.orm import Session
import app.db.database_models as database_models

from app.schemas.model import ProductCreate, ProductUpdate


def get_all_products(db: Session):
    return db.query(database_models.Product).all()


def get_product_by_id(id: int, db: Session):

    return db.query(database_models.Product).filter(
        database_models.Product.id == id
    ).first()


def create_product(product: ProductCreate, db: Session):

    db_product = database_models.Product(**product.model_dump())

    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    return db_product


def replace_product(id: int, product: ProductCreate, db: Session):

    db_product = db.query(database_models.Product).filter(
        database_models.Product.id == id
    ).first()

    if not db_product:
        return None

    db_product.name = product.name
    db_product.description = product.description
    db_product.price = product.price
    db_product.quantity = product.quantity

    db.commit()
    db.refresh(db_product)

    return db_product


def update_product(id: int, product_update: ProductUpdate, db: Session):

    db_product = db.query(database_models.Product).filter(
        database_models.Product.id == id
    ).first()

    if not db_product:
        return None

    if product_update.name is not None:
        db_product.name = product_update.name

    if product_update.description is not None:
        db_product.description = product_update.description

    if product_update.price is not None:
        db_product.price = product_update.price

    if product_update.quantity is not None:
        db_product.quantity = product_update.quantity

    db.commit()
    db.refresh(db_product)

    return db_product


def delete_product(id: int, db: Session):

    db_product = db.query(database_models.Product).filter(
        database_models.Product.id == id
    ).first()

    if not db_product:
        return False

    db.delete(db_product)
    db.commit()

    return True