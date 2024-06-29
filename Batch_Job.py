import os
import logging
from csv_reader import CSVReader
from database_manager import DatabaseManager
from config import Config
from logger import setup_logger

def main():
    setup_logger()
    logger = logging.getLogger(__name__)

    try:
        logger.info("Starting housing data import batch job")

        csv_reader = CSVReader(Config.CSV_FILE_PATH)
        data = csv_reader.read_csv()

        db_manager = DatabaseManager(Config.DB_FOLDER, Config.DB_NAME)
        db_manager.create_table()
        db_manager.insert_data(data)

        logger.info("Housing data import completed successfully")
    except Exception as e:
        logger.error(f"An error occurred during the batch job: {str(e)}")
        raise

if __name__ == "__main__":
    main()