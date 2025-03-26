from sqlalchemy import Column, Integer, String, SmallInteger, Real, Numeric, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from ..database import Base
class Product(Base):
    __tablename__ = 'products'

    ProductID = Column(Integer, primary_key=True)
    ProductName = Column(String)
    SupplierID = Column(Integer, ForeignKey('suppliers.SupplierID'))
    CategoryID = Column(Integer, ForeignKey('categories.CategoryID'))
    QuantityPerUnit = Column(String)
    UnitPrice = Column(Numeric)
    UnitsInStock = Column(SmallInteger)
    UnitsOnOrder = Column(SmallInteger)
    ReorderLevel = Column(SmallInteger)
    Discontinued = Column(Boolean)

    # İlişkiler
    category = relationship("Category", back_populates="products")
    order_details = relationship("OrderDetail", back_populates="product")