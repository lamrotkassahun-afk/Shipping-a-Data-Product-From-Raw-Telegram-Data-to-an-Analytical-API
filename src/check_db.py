# Save as check_db.py and run: python check_db.py
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()
try:
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS")
    )
    print("Database connection successful!")
    conn.close()
except Exception as e:
    print(f"Connection failed: {e}")