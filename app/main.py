from fastapi import FastAPI
from app.routes import public, users
from app.database import engine
from app.models import Base

# Create database table xd
Base.metadata.create_all(bind=engine)


app = FastAPI(swagger_ui_parameters={"syntaxHighlight": False})
app = FastAPI()

# basic routing
app.include_router(users.router)
app.include_router(public.router)