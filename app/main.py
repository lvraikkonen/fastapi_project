from fastapi import FastAPI
from app.db import base, session
from app.routers import auth, example

app = FastAPI()


@app.on_event("startup")
def startup_event():
    base.Base.metadata.create_all(bind=session.engine)
    

app.include_router(example.router, prefix='/api/v1', tags=["examples"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)