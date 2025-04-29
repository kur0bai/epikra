from fastapi import FastAPI
from app.routes import public, users
from app.core.database import engine
from app.models.user import Base

# Create database table xd
Base.metadata.create_all(bind=engine)

# documentation hehe
app = FastAPI(swagger_ui_parameters={"syntaxHighlight": False})
app = FastAPI()

# basic routing
app.include_router(users.router)
app.include_router(public.router)

@app.get("/")
def read_root():
    return {"message": "Hello World"}