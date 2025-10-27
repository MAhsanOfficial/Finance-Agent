# models.py
from sqlalchemy import Column, Integer, String, Float
from database import Base

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(String, index=True, nullable=False)
    customer_name = Column(String, nullable=True)
    amount = Column(Float, nullable=True)
    status = Column(String, nullable=True)
    tx_id = Column(String, nullable=True)
