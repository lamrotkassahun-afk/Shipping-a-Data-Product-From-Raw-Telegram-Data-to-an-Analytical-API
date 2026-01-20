import os
import subprocess
from dagster import op, job, schedule, In, DefaultScheduleStatus

# Get the absolute path to your project root
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# --- OPERATIONS (OPS) ---

@op
def scrape_telegram_data():
    """Step 1: Run telegram.py using the explicit virtual environment python."""
    # This ensures we use the Python that has all your libraries installed
    venv_python = os.path.join(PROJECT_ROOT, ".venv", "Scripts", "python.exe")
    script_path = os.path.join(PROJECT_ROOT, "scripts", "telegram.py")
    
    # Run the script
    subprocess.run([venv_python, script_path], cwd=PROJECT_ROOT, check=True)
    return "Scraping Complete"

@op(ins={"start": In()})
def load_raw_to_postgres(start):
    """Step 2: Run load_to_postgres.py located in the scripts folder."""
    script_path = os.path.join(PROJECT_ROOT, "scripts", "load_to_postgres.py")
    subprocess.run(["python", script_path], cwd=PROJECT_ROOT, check=True)
    return "Loading Complete"

@op(ins={"start": In()})
def run_yolo_enrichment(start):
    """Step 3: Run yolo_detect.py located in the src folder."""
    # Mapped to 'src' folder as requested
    script_path = os.path.join(PROJECT_ROOT, "src", "yolo_detect.py")
    subprocess.run(["python", script_path], cwd=PROJECT_ROOT, check=True)
    return "YOLO Complete"

@op(ins={"start": In()})
def run_dbt_transformations(start):
    """Step 4: Execute dbt models."""
    warehouse_dir = os.path.join(PROJECT_ROOT, "medical_warehouse")
    # Seed loads the CSV results from YOLO into Postgres
    subprocess.run(["dbt", "seed", "--full-refresh"], cwd=warehouse_dir, check=True)
    # Run builds the analytical tables
    subprocess.run(["dbt", "run"], cwd=warehouse_dir, check=True)
    return "DBT Complete"

# --- JOB GRAPH ---

@job
def medical_data_pipeline():
    """Connects the steps: scripts/ -> scripts/ -> src/ -> warehouse/"""
    scraped = scrape_telegram_data()
    loaded = load_raw_to_postgres(scraped)
    enriched = run_yolo_enrichment(loaded)
    run_dbt_transformations(enriched)

# --- SCHEDULING ---

@schedule(
    cron_schedule="0 0 * * *", 
    job=medical_data_pipeline,
    default_status=DefaultScheduleStatus.RUNNING
)
def daily_medical_update():
    """Automates the entire pipeline daily at midnight."""
    return {}