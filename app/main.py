
from wait_for_db import wait_for_postgres

# helper for wait for postgress connection
wait_for_postgres()

from fastapi import FastAPI
from app.routes import public, users, auth
from app.core.database import engine
from app.models.user import Base

# Create database table xd
Base.metadata.create_all(bind=engine)

# documentation hehe
app = FastAPI(swagger_ui_parameters={"syntaxHighlight": False})

# basic routing
app.include_router(users.router)
app.include_router(public.router)
app.include_router(auth.router)
