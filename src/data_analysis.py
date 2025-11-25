import pandas as pd

def filter_data(df, column, value):
    """
    Filters the DataFrame where the column matches the value (case-insensitive).
    
    Args:
        df (pd.DataFrame): The dataset.
        column (str): The column to filter on.
        value (str/int): The value to match.
        
    Returns:
        pd.DataFrame: The filtered view.
    """
    # Handle empty DataFrame
    if df.empty:
        return pd.DataFrame()
    
    if column not in df.columns:
        print(f"Warning: Column {column} not found.")
        return pd.DataFrame() # Return empty if column missing
    
    # Case-insensitive filtering for string values
    if isinstance(value, str):
        # Convert both column values and search value to lowercase for comparison
        mask = df[column].astype(str).str.lower() == value.lower()
        return df[mask]
    else:
        # For non-string values, use exact matching
        return df[df[column] == value]

def calculate_stats(df, column):
    """
    Calculates Mean, Min, and Max for a numeric column.
    
    Args:
        df (pd.DataFrame): The dataset.
        column (str): The name of the numeric column (e.g. '2021').
        
    Returns:
        dict: A dictionary with 'mean', 'min', 'max', or None if invalid.
    """
    # Handle empty DataFrame
    if df.empty:
        return None
    
    if column not in df.columns:
        return None
        
    try:
        series = df[column]
        stats = {
            'mean': series.mean(),
            'min': series.min(),
            'max': series.max(),
            'count': series.count()
        }
        return stats
    except Exception as e:
        print(f"Error calculating stats: {e}")
        return None