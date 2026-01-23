import time
import psycopg2
import os

def wait_for_postgres():
    max_retries = 20
    wait_seconds = 2

    db_host = os.getenv("POSTGRES_HOST", "localhost")
    db_port = os.getenv("POSTGRES_PORT", 5432)
    db_name = os.getenv("POSTGRES_DB")
    db_user = os.getenv("POSTGRES_USER")
    db_pass = os.getenv("POSTGRES_PASSWORD")

    if os.getenv("ENV") != "ci":
        for i in range(max_retries):
            try:
                conn = psycopg2.connect(
                    host=db_host,
                    port=db_port,
                    dbname=db_name,
                    user=db_user,
                    password=db_pass
                )
                conn.close()
                print("✅ Postgres is ready!")
                return
            except psycopg2.OperationalError as e:
                print(f"⏳ Waiting for Postgres ({i+1}/{max_retries})... {e}")
                time.sleep(wait_seconds)
        raise Exception("❌ Could not connect to Postgres after several retries.")
