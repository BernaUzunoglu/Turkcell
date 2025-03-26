from sqlalchemy import Column, Integer, SmallInteger, Real, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base

class OrderDetail(Base):
    __tablename__ = 'order_details'

    OrderID = Column(Integer, ForeignKey('orders.OrderID'), primary_key=True)
    ProductID = Column(Integer, ForeignKey('products.ProductID'), primary_key=True)
    UnitPrice = Column(Numeric)
    Quantity = Column(SmallInteger)
    Discount = Column(Real)

    # İlişkiler
    order = relationship("Order", back_populates="order_details")
    product = relationship("Product", back_populates="order_details")