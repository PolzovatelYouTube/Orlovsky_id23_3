from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.auth import router as auth_router
from app.api.binary_image import router as binary_image_router
from app.db.session import create_db_and_tables

app = FastAPI(title="Binarization API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router, prefix="/api")
app.include_router(binary_image_router, prefix="/api")
from app.api.tasks import router as tasks_router
app.include_router(tasks_router, prefix="/api/tasks")

@app.on_event("startup")
async def startup_event():
    create_db_and_tables()

@app.get("/")
def read_root():
    return {"message": "Welcome to Binarization API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)