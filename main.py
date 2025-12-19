from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from app.models.eleven import create_tables
from app.routers.eleven_router import router as eleven_router

app = FastAPI(title="11", description="Implementation of 11", version="0.1.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(eleven_router)

@app.get("/")
async def root():
    return {"message": "11"}

@app.on_event("startup")
async def on_startup():
    create_tables()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)