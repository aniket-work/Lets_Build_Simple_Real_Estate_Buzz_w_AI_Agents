import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    CSV_FILE_PATH = os.path.join(BASE_DIR, "staging", "housing.csv")
    DB_FOLDER = os.path.join(BASE_DIR, "database")
    DB_NAME = "housing.db"
    LOG_FOLDER = os.path.join(BASE_DIR, "logs")
    LOG_FILE = os.path.join(LOG_FOLDER, "batch_job.log")
    DATABASE_FOLDER = 'database'
    DB_PATH = os.path.join(BASE_DIR, DATABASE_FOLDER, 'housing.db')
    GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
    MODEL_NAME = "llama3-70b-8192"