from sqlalchemy import Column, Integer, String, DateTime, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base

class Order(Base):
    __tablename__ = 'orders'

    OrderID = Column(Integer, primary_key=True)
    CustomerID = Column(String, ForeignKey('customers.CustomerID'))
    EmployeeID = Column(Integer, ForeignKey('employees.EmployeeID'))
    OrderDate = Column(DateTime)
    RequiredDate = Column(DateTime)
    ShippedDate = Column(DateTime)
    ShipVia = Column(Integer, ForeignKey('shippers.ShipperID'))
    Freight = Column(Numeric)
    ShipName = Column(String)
    ShipAddress = Column(String)
    ShipCity = Column(String)
    ShipRegion = Column(String)
    ShipPostalCode = Column(String)
    ShipCountry = Column(String)

    # İlişkiler
    customer = relationship("Customer", back_populates="orders")
    order_details = relationship("OrderDetail", back_populates="order")