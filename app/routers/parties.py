from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ..db import SessionLocal
from .. import models, schemas
from sqlalchemy import select

router = APIRouter(prefix="/parties", tags=["parties"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("", response_model=List[schemas.Party])
def list_parties(
    role: Optional[str] = Query(default=None, description="producer|buyer|broker"),
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    q = select(models.Party)
    if role:
        bit = {"producer":1, "buyer":2, "broker":4}.get(role.lower())
        if bit:
            q = q.where((models.Party.role_mask.op('&')(bit)) != 0)
    if search:
        like = f"%{search}%"
        q = q.where(models.Party.name.ilike(like))
    rows = db.execute(q).scalars().all()
    return rows

@router.post("", response_model=schemas.Party, status_code=201)
def create_party(payload: schemas.PartyCreate, db: Session = Depends(get_db)):
    p = models.Party(**payload.model_dump())
    db.add(p)
    db.commit()
    db.refresh(p)
    return p
