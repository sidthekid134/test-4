from typing import Optional
from sqlmodel import Field, SQLModel, create_engine, Session

class Eleven(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    value: int = Field(default=11)
    description: str = Field(default="The number 11")

# Database setup
DATABASE_URL = "sqlite:///eleven.db"
engine = create_engine(DATABASE_URL, echo=True)

def create_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session