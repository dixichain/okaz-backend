from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select, func, desc, and_
from typing import Optional
from ..db import SessionLocal
from .. import models, schemas

router = APIRouter(prefix="/deals", tags=["deals"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def compute_totals(qty: float, price: float, fees: float = 0.0, commission: float = 0.0):
    gross = round((qty or 0) * (price or 0), 3)
    net = round(gross - (fees or 0) - (commission or 0), 3)
    return gross, fees or 0.0, commission or 0.0, net

@router.get("", response_model=schemas.DealsPage)
def list_deals(
    from_: Optional[str] = Query(default=None, alias="from"),
    to: Optional[str] = None,
    producer_id: Optional[int] = None,
    buyer_id: Optional[int] = None,
    commodity: Optional[str] = None,
    status: Optional[str] = None,
    page: int = 1,
    limit: int = 50,
    sort: str = "-deal_date",
    db: Session = Depends(get_db)
):
    q = select(models.Deal)
    if from_:
        q = q.where(models.Deal.deal_date >= from_)
    if to:
        q = q.where(models.Deal.deal_date <= to)
    if producer_id:
        q = q.where(models.Deal.producer_id == producer_id)
    if buyer_id:
        q = q.where(models.Deal.buyer_id == buyer_id)
    if commodity:
        q = q.where(models.Deal.commodity == commodity)
    if status:
        q = q.where(models.Deal.status == status)

    # sorting
    if sort.startswith("-"):
        q = q.order_by(desc(getattr(models.Deal, sort[1:], models.Deal.deal_date)))
    else:
        q = q.order_by(getattr(models.Deal, sort, models.Deal.deal_date))

    total = db.execute(select(func.count()).select_from(q.subquery())).scalar() or 0
    rows = db.execute(q.offset((page-1)*limit).limit(limit)).scalars().all()
    return {"items": rows, "page": page, "limit": limit, "total": total}

@router.get("/{id}", response_model=schemas.Deal)
def get_deal(id: int, db: Session = Depends(get_db)):
    row = db.get(models.Deal, id)
    if not row:
        raise HTTPException(status_code=404, detail="Deal not found")
    return row

@router.post("", response_model=schemas.Deal, status_code=201)
def create_deal(payload: schemas.DealCreate, db: Session = Depends(get_db)):
    gross, fees, commission, net = compute_totals(payload.qty, payload.price)
    data = payload.model_dump(exclude={"fees","commissions"})
    d = models.Deal(**data,
                    gross_amount=gross,
                    fees_amount=fees,
                    commission_amount=commission,
                    net_amount=net,
                    status="posted",
                    source="api")
    db.add(d)
    db.commit()
    db.refresh(d)
    return d

@router.put("/{id}", response_model=schemas.Deal)
def update_deal(id: int, payload: schemas.DealCreate, db: Session = Depends(get_db)):
    d = db.get(models.Deal, id)
    if not d:
        raise HTTPException(status_code=404, detail="Deal not found")
    for k, v in payload.model_dump(exclude={"fees","commissions"}).items():
        setattr(d, k, v)
    # recompute
    gross, fees, commission, net = compute_totals(payload.qty, payload.price)
    d.gross_amount = gross
    d.fees_amount = fees
    d.commission_amount = commission
    d.net_amount = net
    db.commit()
    db.refresh(d)
    return d
