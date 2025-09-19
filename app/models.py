from sqlalchemy import Column, BigInteger, Integer, Text, Boolean, Date, Numeric, ForeignKey, JSON
from sqlalchemy.orm import relationship
from .db import Base

class Party(Base):
    __tablename__ = "parties"
    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(Text, nullable=False)
    code = Column(Text)
    phone = Column(Text)
    address = Column(Text)
    role_mask = Column(Integer, nullable=False, default=0)
    is_active = Column(Boolean, nullable=False, default=True)
    # timestamps exist in DB, but we don't need to map them here for POC

class Deal(Base):
    __tablename__ = "deals"
    id = Column(BigInteger, primary_key=True, index=True)
    deal_date = Column(Date, nullable=False)
    asm_id = Column(Text)
    doc_no = Column(Text)
    type = Column(Text)
    type2 = Column(Text)
    kind = Column(Text)
    commodity = Column(Text)
    qty = Column(Numeric(18,3), nullable=False, default=0)
    unit = Column(Text)
    price = Column(Numeric(18,3), nullable=False, default=0)
    currency = Column(Text, nullable=False, default="SAR")
    producer_id = Column(BigInteger, ForeignKey("parties.id"))
    buyer_id = Column(BigInteger, ForeignKey("parties.id"))
    gross_amount = Column(Numeric(18,3), nullable=False, default=0)
    fees_amount = Column(Numeric(18,3), nullable=False, default=0)
    commission_amount = Column(Numeric(18,3), nullable=False, default=0)
    net_amount = Column(Numeric(18,3), nullable=False, default=0)
    status = Column(Text, nullable=False, default="posted")
    source = Column(Text, nullable=False, default="import")
    raw_legacy = Column(JSON)
