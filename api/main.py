from fastapi import FastAPI, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from .database import get_db
import logging
import time
import os

# Ensure the logs directory exists
if not os.path.exists("logs"):
    os.makedirs("logs")

# SETUP STRUCTURED LOGGING
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/api_access.log"), # Permanent file record
        logging.StreamHandler()                     # Real-time terminal output
    ]
)
logger = logging.getLogger("MedicalAPI")

app = FastAPI(title="Pharmaceutical Sales API")

# LOGGING MIDDLEWARE (The Flight Recorder)
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    response = await call_next(request)
    
    process_time = time.time() - start_time
    
    # We use a simpler way to format the string to avoid the ValueError
    log_message = "Method: {} Path: {} Status: {} Duration: {:.2f}s".format(
        request.method, 
        request.url.path, 
        response.status_code, 
        process_time
    )
    
    logger.info(log_message)
    return response

@app.get("/")
def read_root():
    return {"message": "Welcome to the Medical Analytical API"}

@app.get("/api/messages")
def get_messages(db: Session = Depends(get_db)):
    """
    This endpoint queries the dbt Mart directly!
    """
    # Note: We use the 'main' schema prefix here
    query = text("SELECT * FROM main.fct_messages")
    result = db.execute(query).mappings().all()
    return result

@app.get("/api/reports/top-channels")
def get_top_channels(db: Session = Depends(get_db)):
    """
    An analytical endpoint showing view counts by channel
    """
    query = text("""
        SELECT channel_name, sum(view_count) as total_views
        FROM main.fct_messages m
        JOIN main.dim_channels c ON m.channel_key = c.channel_key
        GROUP BY channel_name
        ORDER BY total_views DESC
    """)
    result = db.execute(query).mappings().all()
    return result

@app.get("/api/search")
def search_messages(query: str, db: Session = Depends(get_db)):
    """
    Allows users to search for specific drugs or products.
    Example: /api/search?query=Paracetamol
    """
    logger.info(f"Searching for keyword: {query}")
    sql = text("SELECT * FROM main.fct_messages WHERE message_text ILIKE :q")
    result = db.execute(sql, {"q": f"%{query}%"}).mappings().all()
    return result

@app.get("/api/reports/summary")
def get_summary_stats(db: Session = Depends(get_db)):
    """
    Returns high-level KPI summary for the dashboard.
    """
    query = text("""
        SELECT 
            count(*) as total_messages,
            sum(view_count) as total_views,
            avg(view_count)::int as avg_views_per_post
        FROM main.fct_messages
    """)
    return db.execute(query).mappings().first()