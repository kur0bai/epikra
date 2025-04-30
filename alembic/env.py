from alembic import context
from sqlalchemy import engine_from_config, pool
from logging.config import fileConfig
from sqlalchemy.engine.url import URL
import os

# Alembic config
config = context.config
fileConfig(config.config_file_name)

# DATABASE URL
DATABASE_URL = URL.create(
    drivername="postgresql+psycopg2",
    username=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    host=os.getenv("POSTGRES_HOST", "localhost"),
    port=os.getenv("POSTGRES_PORT", "5432"),
    database=os.getenv("POSTGRES_DB"),
)

config.set_main_option("sqlalchemy.url", str(DATABASE_URL))
