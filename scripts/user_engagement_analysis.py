import psycopg2
import pandas as pd
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

def load_data_from_postgres(query):
    try:
        # Fetching credentials from environment variables
        connection = psycopg2.connect(
            host=os.getenv('DB_HOST'),
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASS')
        )
        
        # Load data from PostgreSQL
        df = pd.read_sql_query(query, connection)
        connection.close()
        return df
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
