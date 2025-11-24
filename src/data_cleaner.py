import pandas as pd

def clean_health_data(df):
    """
    Cleans the health data DataFrame.
    1. Removes brackets and notes from all column names (e.g., '[Note 3]'). Already done manually on dataset, but kept for future robustness.
    2. Fills missing numeric values with the column mean.
    
    Args:
        df (pd.DataFrame): The raw data.
        
    Returns:
        pd.DataFrame: The cleaned data.
    """
    # Create a copy to avoid SettingWithCopy warnings on the original df
    clean_df = df.copy()
    
    # Handle empty DataFrame
    if clean_df.empty:
        return clean_df
    
    # 1. Clean column names - remove brackets and everything inside them
    # Also strip any extra whitespace
    clean_df.columns = clean_df.columns.str.replace(r'\s*\[.*?\]\s*', '', regex=True).str.strip()
    
    # 2. Handle missing values
    # For numeric columns, fill with the mean of that column
    numeric_cols = clean_df.select_dtypes(include=['number']).columns
    for col in numeric_cols:
        # Fill NaN with column mean, or 0 if the column is all NaN
        mean_val = clean_df[col].mean()
        if pd.isna(mean_val):
            clean_df[col] = clean_df[col].fillna(0)
        else:
            clean_df[col] = clean_df[col].fillna(mean_val)
    
    # For non-numeric columns, fill with "Unknown" 
    clean_df = clean_df.fillna("Unknown")
    
    return clean_df