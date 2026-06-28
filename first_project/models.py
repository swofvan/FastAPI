from sqlalchemy import Column, Integer, String, Float

from sqlalchemy.orm import declarative_base

Base = declarative_base()  # Every SQLAlchemy model must inherit from Base.

class Products(Base):
    __tablename__ = "products"   # Create a table named products

    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String(100))
    category = Column(String(100))
    price = Column(Float)
    quantity = Column(Integer)