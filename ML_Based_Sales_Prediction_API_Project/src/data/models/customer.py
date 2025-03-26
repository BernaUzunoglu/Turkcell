from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from ..database import Base
class Customer(Base):
    __tablename__ = 'customers'

    CustomerID = Column(String, primary_key=True)
    CompanyName = Column(String)
    ContactName = Column(String)
    ContactTitle = Column(String)
    Address = Column(String)
    City = Column(String)
    Region = Column(String)
    PostalCode = Column(String)
    Country = Column(String)
    Phone = Column(String)
    Fax = Column(String)

    # İlişkiler
    orders = relationship("Order", back_populates="customer")