import psycopg2
from dotenv import load_dotenv
import os
# Load environment variables from .env file
load_dotenv()

def get_env_vars(*args):
    return [os.getenv(arg) for arg in args]

DB_HOST, DB_NAME, DB_USERNAME, DB_PASSWORD, DB_PORT = get_env_vars('DB_HOST', 'DB_NAME', 'DB_USERNAME', 'DB_PASSWORD', 'DB_PORT')
# Function to connect to the PostgreSQL database
def connect_to_db():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USERNAME,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )

# Function to execute a SQL query
def insert_programming_language(db_connection, name, summary, embeddings):
    try: 
        print(db_connection)
        print(name)
        print(embeddings)
        cursor = db_connection.cursor()
        # Example query - modify according to your actual requirements
        query = "INSERT INTO programming_languages(name, summary, text_embeddings) VALUES (%s, %s, %s)"
        cursor.execute(query, (name, summary, embeddings, ))
        db_connection.commit()
    except psycopg2.OperationalError as e:
        print(f"Database connection failed: {e}")
    finally:
        cursor.close()

def execute_fetchall(embeddings):
    db_connection = connect_to_db()
    try: 
        cursor = db_connection.cursor()
        # Example query - modify according to your actual requirements
        query = "SELECT name, summary, 1 - (text_embeddings <=> %s) as similarity FROM programming_languages ORDER BY similarity DESC LIMIT 5";
        cursor.execute(query, (f'{embeddings}', ))

        results = cursor.fetchall()
        return results
    except psycopg2.OperationalError as e:
        print(f"Database connection failed: {e}")
    finally:
        cursor.close()
        db_connection.close()