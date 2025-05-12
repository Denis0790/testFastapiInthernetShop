from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated

from slugify import slugify
from sqlalchemy import insert, select, update
from sqlalchemy.orm import Session

from app.models import Product, Category
from app.schemas import CreateProduct
from app.backend.db_depends import get_db

router = APIRouter(prefix='/products', tags=['products'])


@router.get('/')
async def all_products(db: Annotated[Session, Depends(get_db)]):
    products = db.scalars(select(Product).where(Product.is_active == True, Product.stock > 0)).all()
    if products is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Products is not founded.')
    return products


@router.post('/create')
async def create_product(db: Annotated[Session, Depends(get_db)], create_product: CreateProduct):
    db.execute(insert(Product).values(
        name=create_product.name,
        slug=slugify(create_product.name),
        description=create_product.description,
        price=create_product.price,
        image_url=create_product.image_url,
        stock=create_product.stock,
        category_id=create_product.category,
        rating=0
    ))
    db.commit()
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Successful'
    }


@router.get('/{category_slug}')
async def product_by_category(db: Annotated[Session, Depends(get_db)], category_slug: str):
    category = db.scalar(select(Category).where(Category.slug == category_slug))
    if category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not found category.')
    subcategories = db.scalars(select(Category).where(Category.parent_id == category.id)).all()
    categories_and_subcategories = [category.id] + [i.id for i in subcategories]
    products_category = db.scalars(
        select(Product).where(Product.category_id.in_(categories_and_subcategories), Product.is_active == True,
                              Product.stock > 0)).all()
    return products_category


@router.get('/detail/{product_slug}')
async def product_detail(db: Annotated[Session, Depends(get_db)], product_slug: str):
    product = db.scalar(select(Product).where(Product.slug == product_slug, Product.is_active == True,
                                              Product.stock > 0))
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Product is no founded.')
    return product


@router.put('/detail/{product_slug}')
async def update_product(db: Annotated[Session, Depends(get_db)], product_slug: str, update_product_model: CreateProduct):
    product = db.scalar(select(Product).where(Product.slug == product_slug))
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Product is no founded.')
    db.execute(update(Product).where(Product.slug == product_slug).values(
        name=update_product_model.name,
        description=update_product_model.description,
        price=update_product_model.price,
        image_url=update_product_model.image_url,
        stock=update_product_model.stock,
        category=update_product_model.category,
        slug=slugify(update_product_model.name)
    ))
    db.commit()
    return {'status_code': status.HTTP_200_OK,
            'transaction': 'Product was updated.'}


@router.delete('/delete')
async def delete_product(db: Annotated[Session, Depends(get_db)], product_id: int):
    product = db.scalar(select(Product).where(Product.id == product_id))
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Product is not found.')
    db.execute(update(Product).where(Product.id == product_id).values(is_active=False))
    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Product deleted.'
    }
