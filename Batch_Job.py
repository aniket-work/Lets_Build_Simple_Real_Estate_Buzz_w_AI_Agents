import os
import pandas as pd
import sqlite3
from config import Config


def process_csv_files():
    staging_dir = Config.STAGING_DIR
    db_path = Config.DB_PATH

    # Ensure the database directory exists
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    # Connect to the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Process each CSV file in the staging directory
    for filename in os.listdir(staging_dir):
        if filename.endswith('.csv'):
            file_path = os.path.join(staging_dir, filename)
            table_name = os.path.splitext(filename)[0]

            # Read the CSV file
            df = pd.read_csv(file_path)

            # Create the table (drop if exists)
            cursor.execute(f"DROP TABLE IF EXISTS {table_name}")

            # Get column names and types
            columns = []
            for column in df.columns:
                if df[column].dtype == 'int64':
                    col_type = 'INTEGER'
                elif df[column].dtype == 'float64':
                    col_type = 'REAL'
                else:
                    col_type = 'TEXT'
                columns.append(f"{column} {col_type}")

            # Create the table
            create_table_query = f"CREATE TABLE {table_name} ({', '.join(columns)})"
            cursor.execute(create_table_query)

            # Insert data into the table
            df.to_sql(table_name, conn, if_exists='replace', index=False)

            print(f"Processed {filename} and created table {table_name}")

    # Commit changes and close the connection
    conn.commit()
    conn.close()

    print("Batch job completed successfully")


if __name__ == "__main__":
    process_csv_files()