import os
import json
import psycopg2
from sqlalchemy import create_engine
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

# Database connection details
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5434") # As confirmed in your pgAdmin
DB_NAME = os.getenv("DB_NAME", "medical_db")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS")

def load_data():
    # 1. Connect to PostgreSQL to ensure the raw schema exists
    try:
        conn = psycopg2.connect(
            host=DB_HOST, 
            port=DB_PORT, 
            database=DB_NAME, 
            user=DB_USER, 
            password=DB_PASS
        )
        cur = conn.cursor()
        cur.execute("CREATE SCHEMA IF NOT EXISTS raw;")
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Initial DB connection failed: {e}")
        return

    # 2. Setup SQLAlchemy engine for pandas
    engine = create_engine(f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}')
    
    # Path to your data lake from Task 1
    data_path = "data/raw/telegram_messages"

    # 3. Walk through directories and load message files
    for root, dirs, files in os.walk(data_path):
        for file in files:
            # SKIP manifest.json to avoid column mismatch errors
            if file.endswith(".json") and file != "manifest.json":
                file_path = os.path.join(root, file)
                
                # USE utf-8 encoding to support Amharic characters
                with open(file_path, 'r', encoding='utf-8') as f:
                    try:
                        data = json.load(f)
                        
                        # Ensure data is a list for DataFrame conversion
                        if isinstance(data, dict):
                            data = [data]
                            
                        df = pd.DataFrame(data)
                        
                        # Load into the raw schema table
                        df.to_sql(
                            'telegram_messages', 
                            engine, 
                            schema='raw', 
                            if_exists='append', 
                            index=False
                        )
                        print(f"Successfully loaded: {file}")
                    except Exception as e:
                        print(f"Error processing {file}: {e}")

if __name__ == "__main__":
    load_data()