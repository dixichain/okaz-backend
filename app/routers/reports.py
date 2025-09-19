from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import Optional, List
from ..db import SessionLocal
from .. import schemas

router = APIRouter(prefix="/reports", tags=["reports"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/sales-summary", response_model=List[schemas.SalesSummaryRow])
def sales_summary(
    by: str = Query(default="day", enum=["day","producer","buyer","commodity"]),
    from_: Optional[str] = Query(default=None, alias="from"),
    to: Optional[str] = None,
    party_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    if by == "day":
        base = "SELECT deal_date::date AS key, SUM(gross_amount) AS gross, SUM(commission_amount) AS commission, SUM(fees_amount) AS fees, SUM(net_amount) AS net FROM deals WHERE status IN ('posted','reconciled')"
        group = " GROUP BY key ORDER BY key"
    elif by == "producer":
        base = "SELECT COALESCE(producer_id::text,'') AS key, SUM(gross_amount) AS gross, SUM(commission_amount) AS commission, SUM(fees_amount) AS fees, SUM(net_amount) AS net FROM deals WHERE status IN ('posted','reconciled')"
        group = " GROUP BY key ORDER BY key"
    elif by == "buyer":
        base = "SELECT COALESCE(buyer_id::text,'') AS key, SUM(gross_amount) AS gross, SUM(commission_amount) AS commission, SUM(fees_amount) AS fees, SUM(net_amount) AS net FROM deals WHERE status IN ('posted','reconciled')"
        group = " GROUP BY key ORDER BY key"
    else:  # commodity
        base = "SELECT COALESCE(commodity,'') AS key, SUM(gross_amount) AS gross, SUM(commission_amount) AS commission, SUM(fees_amount) AS fees, SUM(net_amount) AS net FROM deals WHERE status IN ('posted','reconciled')"
        group = " GROUP BY key ORDER BY key"

    where_clauses = []
    params = {}
    if from_:
        where_clauses.append("deal_date >= :from_")
        params["from_"] = from_
    if to:
        where_clauses.append("deal_date <= :to")
        params["to"] = to
    if party_id and by in ("producer","buyer"):
        if by == "producer":
            where_clauses.append("producer_id = :party_id")
        else:
            where_clauses.append("buyer_id = :party_id")
        params["party_id"] = party_id

    sql = base
    if where_clauses:
        sql += " AND " + " AND ".join(where_clauses)
    sql += group

    rows = db.execute(text(sql), params).mappings().all()
    # cast keys to str
    return [{"key": str(r["key"]), "gross": float(r["gross"] or 0), "commission": float(r["commission"] or 0), "fees": float(r["fees"] or 0), "net": float(r["net"] or 0)} for r in rows]

@router.get("/statements/producer", response_model=schemas.ProducerStatement)
def producer_statement(
    producer_id: int,
    from_: Optional[str] = Query(default=None, alias="from"),
    to: Optional[str] = None,
    db: Session = Depends(get_db)
):
    sql = "SELECT * FROM deals WHERE status IN ('posted','reconciled') AND producer_id = :pid"
    params = {"pid": producer_id}
    if from_:
        sql += " AND deal_date >= :from_"
        params["from_"] = from_
    if to:
        sql += " AND deal_date <= :to"
        params["to"] = to

    rows = db.execute(text(sql), params).mappings().all()
    subtotal = {"gross":0.0,"commission":0.0,"fees":0.0,"net":0.0}
    for r in rows:
        subtotal["gross"] += float(r.get("gross_amount") or 0)
        subtotal["commission"] += float(r.get("commission_amount") or 0)
        subtotal["fees"] += float(r.get("fees_amount") or 0)
        subtotal["net"] += float(r.get("net_amount") or 0)

    # Minimal shape to match schema
    return {
        "producer_id": producer_id,
        "from": from_,
        "to": to,
        "rows": rows,
        "subtotal": subtotal
    }
