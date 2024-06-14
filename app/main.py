from fastapi import FastAPI
from app.db import base, session
from app.routers import auth, example
from contextlib import asynccontextmanager

app = FastAPI()


# Lifespan context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code here
    print("Starting up...")
    # create database
    base.Base.metadata.create_all(bind=session.engine)
    yield
    # Shutdown code here
    print("Shutting down...")

# Assign the lifespan context manager to the app
app.router.lifespan_context = lifespan

app.include_router(example.router, prefix='/api/v1', tags=["examples"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
