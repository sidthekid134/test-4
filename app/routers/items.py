from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session, select

from ..models.item import Item, ItemCreate, ItemRead, ItemUpdate
from ..database import get_session

router = APIRouter(
    prefix="/items",
    tags=["items"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=List[ItemRead])
def read_items(
    *, 
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
    is_active: Optional[bool] = None
):
    """Get all items with optional filtering"""
    query = select(Item)
    if is_active is not None:
        query = query.where(Item.is_active == is_active)
    
    items = session.exec(query.offset(offset).limit(limit)).all()
    return items


@router.get("/{item_id}", response_model=ItemRead)
def read_item(*, session: Session = Depends(get_session), item_id: int):
    """Get item by ID"""
    item = session.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.post("/", response_model=ItemRead, status_code=status.HTTP_201_CREATED)
def create_item(*, session: Session = Depends(get_session), item: ItemCreate):
    """Create a new item"""
    db_item = Item.from_orm(item)
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item


@router.patch("/{item_id}", response_model=ItemRead)
def update_item(
    *, session: Session = Depends(get_session), item_id: int, item: ItemUpdate
):
    """Update an item"""
    db_item = session.get(Item, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    item_data = item.dict(exclude_unset=True)
    for key, value in item_data.items():
        setattr(db_item, key, value)
    
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(*, session: Session = Depends(get_session), item_id: int):
    """Delete an item"""
    db_item = session.get(Item, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    session.delete(db_item)
    session.commit()
    return None