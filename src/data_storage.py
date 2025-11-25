import sqlite3
import pandas as pd

def save_to_database(df, db_name, table_name="health_data"):
    """
    Saves a Pandas DataFrame to a SQLite database.
    
    Args:
        df (pd.DataFrame): The data to save.
        db_name (str): The database filename (e.g., 'health.db').
        table_name (str): The name of the SQL table.
    """
    conn = None
    try:
        # connect to the database (it will be created if it doesn't exist)
        conn = sqlite3.connect(db_name)
        
        # 'if_exists="replace"' will overwrite the table if it already exists.
        # Use 'append' if you want to add to it.
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        
        print(f"Data successfully saved to {table_name} in {db_name}")
    except Exception as e:
        print(f"Error saving to database: {e}")
    finally:
        # Ensure connection is closed even if error occurs
        if conn:
            conn.close()

def fetch_data_from_db(db_name, table_name="health_data"):
    """
    Reads data from a SQL table into a DataFrame.
    
    Args:
        db_name (str): The database filename.
        table_name (str): The name of the SQL table.
        
    Returns:
        pd.DataFrame: The data from the table, or None if table doesn't exist.
    """
    conn = None
    try:
        conn = sqlite3.connect(db_name)
        
        # Check if table exists first
        cursor = conn.cursor()
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
            (table_name,)
        )
        table_exists = cursor.fetchone()
        
        if not table_exists:
            print(f"Table '{table_name}' does not exist in database.")
            return None
        
        # Table exists, fetch data
        query = f"SELECT * FROM {table_name}"
        df = pd.read_sql(query, conn)
        return df
        
    except Exception as e:
        print(f"Error loading from database: {e}")
        return None
    finally:
        # Ensure connection is closed
        if conn:
            conn.close()