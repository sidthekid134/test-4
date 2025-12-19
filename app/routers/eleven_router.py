from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List

from app.models.eleven import Eleven, get_session

router = APIRouter(prefix="/eleven", tags=["eleven"])

@router.get("/", response_model=int)
async def get_eleven():
    """Return the number 11"""
    return 11

@router.get("/db", response_model=List[Eleven])
async def get_eleven_from_db(session: Session = Depends(get_session)):
    """Get all eleven entries from the database"""
    elevens = session.exec(select(Eleven)).all()
    return elevens

@router.post("/", response_model=Eleven)
async def create_eleven(session: Session = Depends(get_session)):
    """Create a new eleven entry in the database"""
    eleven = Eleven()
    session.add(eleven)
    session.commit()
    session.refresh(eleven)
    return eleven