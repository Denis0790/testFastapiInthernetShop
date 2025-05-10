from app.backend.db import Base
from sqlalchemy import Column, Integer, ForeignKey, Boolean, String, Float
from sqlalchemy.orm import relationship
from app.models import *


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    slug = Column(String, unique=True, index=True)
    description = Column(String)
    price = Column(Integer)
    image_url = Column(String)
    stock = Column(Integer)
    category_id = Column(Integer, ForeignKey('categories.id'))
    rating = Column(Integer)
    is_active = Column(Boolean, default=True)

    category = relationship('Category', back_populates='products')
