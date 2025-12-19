from sqlmodel import Session

from app.database import create_db_and_tables, engine
from app.models.story import Story

def init_db():
    create_db_and_tables()
    
    with Session(engine) as session:
        # Check if we already have stories
        story = session.query(Story).first()
        if story is None:
            print("Creating initial data")
            # Create sample stories
            story1 = Story(
                title="Welcome to Story API",
                description="This is a sample story to demonstrate the API functionality.",
                content="Here you can write the full content of your story. This can be a long text with multiple paragraphs.",
                status="published"
            )
            story2 = Story(
                title="Placeholder Story",
                description="A placeholder story for development and testing purposes.",
                content="This is just placeholder content for testing the API.",
                status="draft"
            )
            session.add(story1)
            session.add(story2)
            session.commit()
            print(f"Created {session.query(Story).count()} sample stories")
        else:
            print(f"Database already contains {session.query(Story).count()} stories")

if __name__ == "__main__":
    print("Initializing the database...")
    init_db()
    print("Database initialized!")