from fastapi import APIRouter, Depends, HTTPException, status
from slugify import slugify
from app.models import *
from app.schemas import CreateCategory
from app.backend.db_depends import get_db
from sqlalchemy.orm import Session
from sqlalchemy import insert, select, update
from typing import Annotated

router = APIRouter(prefix='/category', tags=['category'])


@router.get('/all_categories')
async def all_categories(db: Annotated[Session, Depends(get_db)]):
    categories = db.scalars(select(Category).where(Category.is_active == True)).all()
    return categories


@router.post('/create')
async def create_category(db: Annotated[Session, Depends(get_db)], create_category: CreateCategory):
    db.execute(insert(Category).values(name=create_category.name,
                                       parent_id=create_category.parent_id,
                                       slug=slugify(create_category.name)))
    db.commit()
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Successful'
    }


@router.put('/update_category')
async def update_category(db: Annotated[Session, Depends(get_db)], category_id: int, update_category: CreateCategory):
    category = db.scalar(select(Category).where(Category.id == category_id))
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There is no category found.'
        )
    db.execute(update(Category).where(Category.id == category_id).values(
        name=update_category.name,
        parent_id=update_category.parent_id,
        slug=slugify(update_category.name)
    ))
    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Category update is successful'
    }


@router.delete('/delete')
async def delete_category(db: Annotated[Session, Depends(get_db)], category_id: int):
    category = db.scalar(select(Category).where(Category.id == category_id))
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There is no category found.'
        )
    db.execute(update(Category).where(Category.id == category_id).values(is_active=False))
    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Category delete is successful'
    }


@router.put('/update_is_active')
async def update_is_active(db: Annotated[Session, Depends(get_db)], category_id: int):
    category = db.scalar(select(Category).where(Category.id == category_id))
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There is no category found.'
        )
    db.execute(update(Category).where(Category.id == category_id).values(is_active=True))
    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Category up active is successful'
    }
