from sqlalchemy import Column, String, Integer, LargeBinary
from sqlalchemy.orm import relationship
from ..database import Base
class Category(Base):
    __tablename__ = 'categories'

    CategoryID = Column(Integer, primary_key=True)
    CategoryName = Column(String)
    Description = Column(String)
    Picture = Column(LargeBinary)

    # İlişkiler
    products = relationship("Product", back_populates="category")