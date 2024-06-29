import csv
import logging

class CSVReader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.logger = logging.getLogger(__name__)

    def read_csv(self):
        try:
            with open(self.file_path, 'r') as csvfile:
                reader = csv.DictReader(csvfile)
                data = [row for row in reader]
            self.logger.info(f"Successfully read {len(data)} rows from CSV file")
            return data
        except Exception as e:
            self.logger.error(f"Error reading CSV file: {str(e)}")
            raise