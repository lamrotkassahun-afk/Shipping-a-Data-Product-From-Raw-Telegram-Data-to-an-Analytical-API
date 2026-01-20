from fastapi import FastAPI, HTTPException
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI(title="Medical Data Warehouse API")

# Database Connection Helper
def get_db_connection():
    return psycopg2.connect(
        dbname="medical_db",
        user="your_user",
        password="your_password",
        host="localhost",
        port="5432",
        cursor_factory=RealDictCursor
    )

@app.get("/")
def read_root():
    return {"message": "Welcome to the Medical Telegram Analytics API"}

@app.get("/api/reports/top-products")
def get_top_products():
    conn = get_db_connection()
    cur = conn.cursor()
    # Query your Marts table
    query = """
        SELECT image_category, COUNT(*) as mention_count
        FROM staging_marts.fct_image_detections
        GROUP BY image_category
        ORDER BY mention_count DESC
        LIMIT 5;
    """
    cur.execute(query)
    results = cur.fetchall()
    cur.close()
    conn.close()
    return results