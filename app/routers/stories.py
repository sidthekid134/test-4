from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select

from app.database import get_session
from app.models.story import Story, StoryCreate, StoryRead, StoryUpdate

router = APIRouter(
    prefix="/stories",
    tags=["stories"],
    responses={404: {"description": "Story not found"}},
)


@router.post("", response_model=StoryRead)
def create_story(*, session: Session = Depends(get_session), story: StoryCreate):
    """
    Create a new story.
    """
    db_story = Story.model_validate(story)
    session.add(db_story)
    session.commit()
    session.refresh(db_story)
    return db_story


@router.post("/new", response_model=StoryRead)
def create_new_story(*, session: Session = Depends(get_session), title: str, description: str = ""):
    """
    Create a new story with minimal required information (title and optional description).
    This is a simplified endpoint for the "New story" feature.
    """
    story_data = StoryCreate(title=title, description=description)
    db_story = Story.model_validate(story_data)
    session.add(db_story)
    session.commit()
    session.refresh(db_story)
    return db_story


@router.get("", response_model=List[StoryRead])
def read_stories(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, le=100),
):
    """
    Get all stories with pagination.
    """
    stories = session.exec(select(Story).offset(offset).limit(limit)).all()
    return stories


@router.get("/{story_id}", response_model=StoryRead)
def read_story(*, session: Session = Depends(get_session), story_id: int):
    """
    Get a specific story by ID.
    """
    story = session.get(Story, story_id)
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")
    return story


@router.patch("/{story_id}", response_model=StoryRead)
def update_story(
    *,
    session: Session = Depends(get_session),
    story_id: int,
    story: StoryUpdate,
):
    """
    Update a story.
    """
    db_story = session.get(Story, story_id)
    if not db_story:
        raise HTTPException(status_code=404, detail="Story not found")
    
    story_data = story.model_dump(exclude_unset=True)
    for key, value in story_data.items():
        setattr(db_story, key, value)
    
    db_story.updated_at = datetime.utcnow()
    session.add(db_story)
    session.commit()
    session.refresh(db_story)
    return db_story


@router.delete("/{story_id}")
def delete_story(*, session: Session = Depends(get_session), story_id: int):
    """
    Delete a story.
    """
    story = session.get(Story, story_id)
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")
    
    session.delete(story)
    session.commit()
    return {"ok": True}