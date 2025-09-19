from pydantic import BaseModel, Field
from typing import Optional, List, Literal
from datetime import date

class PartyBase(BaseModel):
    name: str
    code: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    role_mask: int = 0
    is_active: bool = True

class PartyCreate(PartyBase):
    pass

class Party(PartyBase):
    id: int
    class Config:
        from_attributes = True

class FeeInput(BaseModel):
    fee_type: str
    amount: float

class CommissionInput(BaseModel):
    kind: str = "broker"
    rate_pct: Optional[float] = None
    fixed_amount: Optional[float] = None
    base: str = "gross"

class DealBase(BaseModel):
    deal_date: date
    asm_id: Optional[str] = None
    doc_no: Optional[str] = None
    type: Optional[str] = None
    type2: Optional[str] = None
    kind: Optional[str] = None
    commodity: Optional[str] = None
    qty: float = 0
    unit: Optional[str] = None
    price: float = 0
    currency: str = "SAR"
    producer_id: Optional[int] = None
    buyer_id: Optional[int] = None
    raw_legacy: Optional[dict] = None

class DealCreate(DealBase):
    fees: Optional[List[FeeInput]] = None
    commissions: Optional[List[CommissionInput]] = None

class Deal(DealBase):
    id: int
    gross_amount: float
    fees_amount: float
    commission_amount: float
    net_amount: float
    status: str
    source: str
    class Config:
        from_attributes = True

class DealsPage(BaseModel):
    items: List[Deal]
    page: int
    limit: int
    total: int

class SalesSummaryRow(BaseModel):
    key: str
    gross: float
    commission: float
    fees: float
    net: float

class ProducerStatement(BaseModel):
    producer_id: int
    from_: Optional[date] = Field(default=None, alias="from")
    to: Optional[date] = None
    rows: List[Deal]
    subtotal: dict
