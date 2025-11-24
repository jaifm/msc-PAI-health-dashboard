import unittest
import pandas as pd
import numpy as np
import sys
import os

# Add 'src' to the python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from data_cleaner import clean_health_data

class TestDataCleaner(unittest.TestCase):
    
    def setUp(self):
        """Create a mock 'dirty' DataFrame to test with."""
        data = {
            'Area Name': ['City A', 'City B'],
            'Area Type [Note 3]': ['LTLA', 'Region'], # Messy name, manually changed on dataset but kept in test for future robustness.
            '2015': [100.0, np.nan],                  # Missing value
            '2016': [102.0, 98.0]
        }
        self.df = pd.DataFrame(data)

    def test_rename_columns(self):
        """Test that the messy column name is cleaned up."""
        cleaned = clean_health_data(self.df)
        self.assertIn('Area Type', cleaned.columns)
        self.assertNotIn('Area Type [Note 3]', cleaned.columns)

    def test_handle_missing_values(self):
        """Test that NaN values are filled."""
        cleaned = clean_health_data(self.df)
        # Check that there are no null values left
        self.assertFalse(cleaned.isnull().values.any())

    def test_multiple_messy_columns(self):
        """Test cleaning multiple columns with messy names."""
        data = {
            'Area Name [Note 1]': ['City A', 'City B'],
            'Area Type [Note 3]': ['LTLA', 'Region'],
            '2015 [Note 2]': [100.0, 98.0]
        }
        df = pd.DataFrame(data)
        cleaned = clean_health_data(df)
        
        # Check that all brackets and notes are removed
        for col in cleaned.columns:
            self.assertNotIn('[', col, f"Column {col} should not contain '['")
            self.assertNotIn(']', col, f"Column {col} should not contain ']'")

    def test_all_nan_column(self):
        """Test handling of a column with all NaN values."""
        data = {
            'Area Name': ['City A', 'City B'],
            '2015': [np.nan, np.nan],
            '2016': [100.0, 98.0]
        }
        df = pd.DataFrame(data)
        cleaned = clean_health_data(df)
        
        # Should handle all-NaN column without errors
        self.assertIsInstance(cleaned, pd.DataFrame)
        self.assertFalse(cleaned.isnull().values.any())

    def test_non_messy_columns_unchanged(self):
        """Test that clean column names remain unchanged."""
        data = {
            'Area Name': ['City A', 'City B'],
            'Area Code': ['E001', 'E002'],
            '2015': [100.0, 98.0]
        }
        df = pd.DataFrame(data)
        cleaned = clean_health_data(df)
        
        # These columns should still exist with same names
        self.assertIn('Area Name', cleaned.columns)
        self.assertIn('Area Code', cleaned.columns)
        self.assertIn('2015', cleaned.columns)

    def test_data_types_preserved(self):
        """Test that numeric columns remain numeric after cleaning."""
        cleaned = clean_health_data(self.df)
        
        # Year columns should be numeric
        self.assertTrue(pd.api.types.is_numeric_dtype(cleaned['2015']))
        self.assertTrue(pd.api.types.is_numeric_dtype(cleaned['2016']))

    def test_empty_dataframe(self):
        """Test handling of an empty DataFrame."""
        empty_df = pd.DataFrame()
        cleaned = clean_health_data(empty_df)
        
        # Should return empty DataFrame without errors
        self.assertIsInstance(cleaned, pd.DataFrame)
        self.assertEqual(len(cleaned), 0)

    def test_structure_maintained(self):
        """Test that the DataFrame structure (rows, basic shape) is maintained."""
        cleaned = clean_health_data(self.df)
        
        # Should have same number of rows
        self.assertEqual(len(cleaned), len(self.df))
        # Should have at least the same number of columns (might add or keep same)
        self.assertGreaterEqual(len(cleaned.columns), 2)

    def test_multiple_consecutive_nans(self):
        """Test handling of multiple consecutive NaN values in a row."""
        data = {
            'Area Name': ['City A', 'City B', 'City C'],
            '2015': [100.0, np.nan, np.nan],
            '2016': [102.0, np.nan, 95.0],
            '2017': [103.0, 99.0, 96.0]
        }
        df = pd.DataFrame(data)
        cleaned = clean_health_data(df)
        
        # Should handle multiple NaNs without errors
        self.assertFalse(cleaned.isnull().values.any())
        self.assertEqual(len(cleaned), 3)

    def test_all_nan_row(self):
        """Test handling of rows with all NaN values in numeric columns."""
        data = {
            'Area Name': ['City A', 'City B', 'City C'],
            '2015': [100.0, np.nan, 98.0],
            '2016': [102.0, np.nan, 99.0]
        }
        df = pd.DataFrame(data)
        cleaned = clean_health_data(df)
        
        # Should handle without crashing
        self.assertIsInstance(cleaned, pd.DataFrame)

if __name__ == '__main__':
    unittest.main()