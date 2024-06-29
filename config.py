import os

class Config:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    CSV_FILE_PATH = os.path.join(BASE_DIR, "staging", "housing.csv")
    DB_FOLDER = os.path.join(BASE_DIR, "database")
    DB_NAME = "housing.db"
    LOG_FOLDER = os.path.join(BASE_DIR, "logs")
    LOG_FILE = os.path.join(LOG_FOLDER, "batch_job.log")