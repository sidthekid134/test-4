from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship
from .base import BaseModel


class ItemBase(SQLModel):
    name: str = Field(index=True)
    description: Optional[str] = Field(default=None)
    is_active: bool = Field(default=True)


class Item(BaseModel, ItemBase, table=True):
    """Item model for database table"""
    pass


class ItemCreate(ItemBase):
    """Item schema for creation operations"""
    pass


class ItemRead(ItemBase):
    """Item schema for read operations"""
    id: int
    created_at: str
    updated_at: str


class ItemUpdate(SQLModel):
    """Item schema for update operations"""
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None