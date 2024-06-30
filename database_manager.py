import sqlite3
import pandas as pd
from config import Config
from langchain_community.utilities import SQLDatabase

class DatabaseManager:
    def __init__(self):
        self.db_path = Config.DB_PATH
        self.sql_database = SQLDatabase.from_uri(f"sqlite:///{self.db_path}")

    def get_data(self, query):
        conn = sqlite3.connect(self.db_path)
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df

    def get_sql_database(self):
        return self.sql_database