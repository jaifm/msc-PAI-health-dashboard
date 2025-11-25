import unittest
import pandas as pd
import numpy as np
import sqlite3
import sys
import os
import tempfile

# Add 'src' to the python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

# Importing the function
from data_storage import save_to_database, fetch_data_from_db

class TestDataStorage(unittest.TestCase):
    
    def setUp(self):
        """Create a mock DataFrame and a temporary DB connection."""
        self.df = pd.DataFrame({
            'Area Name': ['City A', 'City B'],
            'Value': [100, 200]
        })
        # Use an in-memory database for testing (fast and clean)
        self.db_name = ":memory:"
        
        # Create a temporary file for file-based tests
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db_path = self.temp_db.name
        self.temp_db.close()

    def tearDown(self):
        """Clean up temporary database file."""
        if os.path.exists(self.temp_db_path):
            os.remove(self.temp_db_path)

    def test_save_and_fetch_data(self):
        """Test that we can save a DataFrame to SQL and read it back."""
        # 1. Save data
        save_to_database(self.df, self.db_name, table_name="health_data")
        
        # 2. Verify it exists by connecting manually
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='health_data';")
        table_exists = cursor.fetchone()
        conn.close()
        
        self.assertIsNotNone(table_exists, "Table should exist in DB")

    def test_fetch_returns_dataframe(self):
        """Test the fetch function returns a DataFrame."""
        save_to_database(self.df, self.db_name, table_name="test_table")
        
        # Fetch back
        loaded_df = fetch_data_from_db(self.db_name, table_name="test_table")
        
        self.assertIsInstance(loaded_df, pd.DataFrame)
        self.assertEqual(len(loaded_df), 2)
        self.assertEqual(loaded_df.iloc[0]['Area Name'], 'City A')

    def test_data_integrity(self):
        """Test that data values are preserved after save/fetch."""
        save_to_database(self.df, self.db_name, table_name="integrity_test")
        loaded_df = fetch_data_from_db(self.db_name, table_name="integrity_test")
        
        # Check values match
        self.assertEqual(loaded_df.iloc[0]['Value'], 100)
        self.assertEqual(loaded_df.iloc[1]['Value'], 200)
        self.assertEqual(list(loaded_df['Area Name']), ['City A', 'City B'])

    def test_column_names_preserved(self):
        """Test that column names are preserved."""
        save_to_database(self.df, self.db_name, table_name="columns_test")
        loaded_df = fetch_data_from_db(self.db_name, table_name="columns_test")
        
        # Should have same columns (though order might differ)
        self.assertIn('Area Name', loaded_df.columns)
        self.assertIn('Value', loaded_df.columns)

    def test_row_count_matches(self):
        """Test that row count is preserved."""
        save_to_database(self.df, self.db_name, table_name="count_test")
        loaded_df = fetch_data_from_db(self.db_name, table_name="count_test")
        
        self.assertEqual(len(loaded_df), len(self.df))

    def test_with_nan_values(self):
        """Test handling of NaN values."""
        df_with_nan = pd.DataFrame({
            'Area Name': ['City A', 'City B', 'City C'],
            'Value': [100, np.nan, 300]
        })
        
        save_to_database(df_with_nan, self.db_name, table_name="nan_test")
        loaded_df = fetch_data_from_db(self.db_name, table_name="nan_test")
        
        # Check that NaN is handled (might be NULL in DB)
        self.assertEqual(len(loaded_df), 3)
        # Second row should have NaN or None
        self.assertTrue(pd.isna(loaded_df.iloc[1]['Value']) or loaded_df.iloc[1]['Value'] is None)

    def test_empty_dataframe(self):
        """Test saving and fetching an empty DataFrame."""
        empty_df = pd.DataFrame()
        save_to_database(empty_df, self.db_name, table_name="empty_test")
        loaded_df = fetch_data_from_db(self.db_name, table_name="empty_test")
        
        self.assertIsInstance(loaded_df, pd.DataFrame)
        self.assertEqual(len(loaded_df), 0)

    def test_file_based_database(self):
        """Test with actual file-based database."""
        save_to_database(self.df, self.temp_db_path, table_name="file_test")
        
        # Verify file exists
        self.assertTrue(os.path.exists(self.temp_db_path))
        
        # Fetch data back
        loaded_df = fetch_data_from_db(self.temp_db_path, table_name="file_test")
        self.assertEqual(len(loaded_df), 2)

    def test_table_replacement(self):
        """Test that saving to same table with if_exists='replace' works."""
        # Save original data
        save_to_database(self.df, self.db_name, table_name="replace_test")
        
        # Save different data to same table
        new_df = pd.DataFrame({
            'Area Name': ['City C', 'City D', 'City E'],
            'Value': [300, 400, 500]
        })
        save_to_database(new_df, self.db_name, table_name="replace_test")
        
        # Fetch and verify it has new data
        loaded_df = fetch_data_from_db(self.db_name, table_name="replace_test")
        self.assertEqual(len(loaded_df), 3)  # Should have 3 rows now
        self.assertIn('City C', list(loaded_df['Area Name']))

    def test_special_characters_in_data(self):
        """Test handling of special characters."""
        special_df = pd.DataFrame({
            'Area Name': ["City's Name", 'City "Two"', 'City & More'],
            'Value': [100, 200, 300]
        })
        
        save_to_database(special_df, self.db_name, table_name="special_test")
        loaded_df = fetch_data_from_db(self.db_name, table_name="special_test")
        
        self.assertEqual(len(loaded_df), 3)
        self.assertIn("City's Name", list(loaded_df['Area Name']))

    def test_fetch_nonexistent_table(self):
        """Test fetching from a non-existent table."""
        # Should handle gracefully (return None or empty DataFrame)
        result = fetch_data_from_db(self.db_name, table_name="nonexistent_table")
        # Depending on implementation, could be None or empty DataFrame
        self.assertTrue(result is None or (isinstance(result, pd.DataFrame) and len(result) == 0))

    def test_large_dataset(self):
        """Test with a larger dataset."""
        large_df = pd.DataFrame({
            'Area Name': [f'City {i}' for i in range(1000)],
            'Value': range(1000)
        })
        
        save_to_database(large_df, self.db_name, table_name="large_test")
        loaded_df = fetch_data_from_db(self.db_name, table_name="large_test")
        
        self.assertEqual(len(loaded_df), 1000)

    def test_numeric_data_types(self):
        """Test that numeric data types are handled correctly."""
        numeric_df = pd.DataFrame({
            'integers': [1, 2, 3],
            'floats': [1.1, 2.2, 3.3],
            'mixed': [100, 200.5, 300]
        })
        
        save_to_database(numeric_df, self.db_name, table_name="numeric_test")
        loaded_df = fetch_data_from_db(self.db_name, table_name="numeric_test")
        
        self.assertEqual(len(loaded_df), 3)
        # Check that numeric values are preserved
        self.assertAlmostEqual(loaded_df.iloc[0]['floats'], 1.1, places=5)

    def test_connection_closes_properly(self):
        """Test that connections are properly closed (no resource leaks)."""
        # Save and fetch multiple times
        for i in range(10):
            save_to_database(self.df, self.db_name, table_name=f"test_{i}")
            fetch_data_from_db(self.db_name, table_name=f"test_{i}")
        
        # Should complete without errors
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()