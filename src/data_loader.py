import pandas as pd
import os

def load_csv_data(filepath):
    """
    Loads a CSV file into a Pandas DataFrame.
    
    Args:
        filepath (str): Path to the CSV file.
        
    Returns:
        pd.DataFrame: The loaded data.
        
    Raises:
        FileNotFoundError: If the file does not exist.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"The file {filepath} was not found.")
    
    try:
        # We use standard read_csv
        df = pd.read_csv(filepath)
        return df
    except Exception as e:
        print(f"Error reading file: {e}")
        # Return an empty DataFrame on error to avoid crashing
        return pd.DataFrame()