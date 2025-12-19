from sqlmodel import Session, SQLModel, create_engine
from .config.settings import settings

# Create SQLAlchemy engine
engine = create_engine(
    settings.DATABASE_URL, 
    echo=settings.DEBUG,
    connect_args={"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {}
)


def create_db_and_tables():
    """Initialize database and create tables"""
    SQLModel.metadata.create_all(engine)


def get_session():
    """Dependency for database session"""
    with Session(engine) as session:
        yield session