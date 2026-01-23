
from app.middlewares.logging_middleware import LoggingMiddleware
from app.models.user import Base
from app.core.database import engine
from app.routes import private, users, auth, posts, categories, content_types
from fastapi import FastAPI
from app.routes.dynamic import load_dynamic_routers
from wait_for_db import wait_for_postgres

# helper for wait for postgress connection
if os.getenv("SKIP_DB_WAIT") != "true":
    from wait_for_db import wait_for_postgres
    wait_for_postgres()

# Create database table xd
Base.metadata.create_all(bind=engine)

# documentation hehe
app = FastAPI(swagger_ui_parameters={"syntaxHighlight": False},
              title="Epikra",
              description="Headless, powerful and poisonless CMS API.",
              version="1.0.0")

# Middleware for logging
app.add_middleware(LoggingMiddleware)

# basic routing
app.include_router(users.router)
app.include_router(private.router)
app.include_router(auth.router)
app.include_router(posts.router)
app.include_router(categories.router)
app.include_router(content_types.router, prefix="/content-types")

load_dynamic_routers(app)
