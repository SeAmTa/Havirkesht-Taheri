import os
from pathlib import Path

import pymysql
from dotenv import load_dotenv

# load .env from backend root (one level above /scripts)
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME", "havirkesht")

if not DB_USER or DB_PASSWORD is None:
    raise RuntimeError("DB_USER / DB_PASSWORD not set in .env")

sql_path = Path(__file__).parent / "create_tables.sql"
with open(sql_path, "r", encoding="utf-8") as f:
    sql = f.read()

queries = [q.strip() for q in sql.split(";") if q.strip()]

conn = pymysql.connect(
    host=DB_HOST,
    port=DB_PORT,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME,
    charset="utf8mb4",
    autocommit=False,
)

cursor = conn.cursor()

for q in queries:
    try:
        cursor.execute(q)
    except pymysql.err.OperationalError as e:
        # 1061 = Duplicate key name (index exists)
        if e.args and e.args[0] == 1061:
            print("⚠️ Index already exists — skipped")
            continue
        # 1050 = Table already exists
        if e.args and e.args[0] == 1050:
            print("⚠️ Table already exists — skipped")
            continue
        raise

conn.commit()
cursor.close()
conn.close()

print("✅ All tables and indexes processed successfully.")
