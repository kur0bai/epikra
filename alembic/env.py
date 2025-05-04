from alembic import context
from sqlalchemy import engine_from_config, pool
from logging.config import fileConfig
from sqlalchemy.engine.url import URL
from dotenv import load_dotenv
import os
from app.core.database import Base
from app import models 

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))


# Alembic config
config = context.config
fileConfig(config.config_file_name)

# DATABASE URL
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD= os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_DB = os.getenv("POSTGRES_DB")

DATABASE_URL = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'

config.set_main_option("sqlalchemy.url", str(DATABASE_URL))

target_metadata = Base.metadata

#run migrations
def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()

run_migrations_online()