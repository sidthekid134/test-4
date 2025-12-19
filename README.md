# Story API

A FastAPI application for managing stories with SQLModel.

## Features

- Create, read, update, and delete stories
- Simplified "New story" feature for quick story creation
- SQLModel integration for type-safe database operations
- Modern API with automatic documentation

## Installation

1. Clone this repository
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the application

Run the application with:

```bash
python run.py
```

Access the API at http://localhost:8000

API documentation is available at:
- http://localhost:8000/docs (Swagger UI)
- http://localhost:8000/redoc (ReDoc)

## API Endpoints

- `POST /stories` - Create a new story with all parameters
- `POST /stories/new` - Quick creation of a new story (New story feature)
- `GET /stories` - Get all stories
- `GET /stories/{story_id}` - Get a specific story
- `PATCH /stories/{story_id}` - Update a story
- `DELETE /stories/{story_id}` - Delete a story

## Running Tests

```bash
pytest app/tests/
```