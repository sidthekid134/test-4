from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel


class StoryBase(SQLModel):
    title: str
    description: Optional[str] = None
    content: Optional[str] = None
    status: str = "draft"


class Story(StoryBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default=None)


class StoryCreate(StoryBase):
    pass


class StoryRead(StoryBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]


class StoryUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    content: Optional[str] = None
    status: Optional[str] = None