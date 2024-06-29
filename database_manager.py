import os
import sqlite3
import logging

class DatabaseManager:
    def __init__(self, db_folder, db_name):
        self.db_folder = db_folder
        self.db_name = db_name
        self.db_path = os.path.join(db_folder, db_name)
        self.logger = logging.getLogger(__name__)

    def create_table(self):
        try:
            os.makedirs(self.db_folder, exist_ok=True)
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS housing (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    price INTEGER,
                    area INTEGER,
                    bedrooms INTEGER,
                    bathrooms INTEGER,
                    stories INTEGER,
                    mainroad TEXT,
                    guestroom TEXT,
                    basement TEXT,
                    hotwaterheating TEXT,
                    airconditioning TEXT,
                    parking INTEGER,
                    prefarea TEXT,
                    furnishingstatus TEXT
                )
            ''')
            conn.commit()
            self.logger.info("Housing table created successfully")
        except Exception as e:
            self.logger.error(f"Error creating table: {str(e)}")
            raise
        finally:
            conn.close()

    def insert_data(self, data):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            for row in data:
                cursor.execute('''
                    INSERT INTO housing (
                        price, area, bedrooms, bathrooms, stories, mainroad,
                        guestroom, basement, hotwaterheating, airconditioning,
                        parking, prefarea, furnishingstatus
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    row['price'], row['area'], row['bedrooms'], row['bathrooms'],
                    row['stories'], row['mainroad'], row['guestroom'], row['basement'],
                    row['hotwaterheating'], row['airconditioning'], row['parking'],
                    row['prefarea'], row['furnishingstatus']
                ))
            conn.commit()
            self.logger.info(f"Successfully inserted {len(data)} rows into the database")
        except Exception as e:
            self.logger.error(f"Error inserting data: {str(e)}")
            raise
        finally:
            conn.close()