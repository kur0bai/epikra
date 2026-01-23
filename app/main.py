import os
from fastapi import FastAPI
from app.middlewares.logging_middleware import LoggingMiddleware
from app.routes import private, users, auth, posts, categories, content_types
from app.routes.dynamic import load_dynamic_routers

app = FastAPI(
    swagger_ui_parameters={"syntaxHighlight": False},
    title="Epikra",
    description="Headless, powerful and poisonless CMS API.",
    version="1.0.0",
)

# Middleware
app.add_middleware(LoggingMiddleware)

# Routes
app.include_router(users.router)
app.include_router(private.router)
app.include_router(auth.router)
app.include_router(posts.router)
app.include_router(categories.router)
app.include_router(content_types.router, prefix="/content-types")

load_dynamic_routers(app)


# Startup lifecycle
@app.on_event("startup")
def startup_event():
    if os.getenv("SKIP_DB_WAIT") == "true":
        print("🟡 SKIP_DB_WAIT=true → DB initialization skipped")
        return

    from wait_for_db import wait_for_postgres
    from app.core.database import engine
    from app.models.user import Base

    wait_for_postgres()
    Base.metadata.create_all(bind=engine)
    print("✅ Database ready")
