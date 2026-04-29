# models/product.py
from sqlalchemy import Column, Integer, String , DateTime ,func
from database.db import Base

class Product(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String(100), nullable=False)
    product_brand = Column(String(200), nullable=False)
    product_category = Column(String(200), nullable=False)
    product_description = Column(String(500))
    price = Column(String(500))
    product_image = Column(String, nullable=True)
    product_rating = Column(String, nullable=True)
    
    

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    
    