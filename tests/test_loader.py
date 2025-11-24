import unittest, os, sys
import pandas as pd

# Adjust the path to import from src directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from data_loader import load_csv_data

class TestDataLoader(unittest.TestCase):
    
    def setUp(self):
        """Runs before each test. Useful for setup."""
        self.filename = "data/overall_health_index.csv"

    def test_load_csv_structure(self):
        """Test that data loads as a pandas DataFrame."""
        df = load_csv_data(self.filename)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertGreater(len(df), 0, "DataFrame should not be empty")
        self.assertGreater(len(df.columns), 0, "DataFrame should have columns")

    def test_load_csv_content(self):
        """Test that specific columns from the health index file exist."""
        df = load_csv_data(self.filename)
        
        # Check for expected columns
        self.assertIn('Area Name', df.columns)
        self.assertIn('Area Code', df.columns)
        self.assertIn('2015', df.columns) 
        
        # Check if the values match ('ENGLAND' is first)
        self.assertEqual(df.iloc[0]['Area Name'], 'ENGLAND')

    def test_file_not_found(self):
        """Test that the loader handles missing files gracefully."""
        with self.assertRaises(FileNotFoundError):
            load_csv_data("data/ghost_file.csv")

    def test_all_expected_columns(self):
        """Test that all expected columns are present."""
        df = load_csv_data(self.filename)
        
        expected_columns = ['Area Code', 'Area Name', 'Area Type', 
                          '2015', '2016', '2017', '2018', '2019', '2020', '2021']
        for column in expected_columns:
            self.assertIn(column, df.columns, f"Column '{column}' should exist")

    def test_multiple_rows_loaded(self):
        """Test that multiple rows are loaded, not just the first."""
        df = load_csv_data(self.filename)
        self.assertGreater(len(df), 10, "Should load more than 10 rows")
        
        # Verify second row is different from first
        self.assertNotEqual(df.iloc[0]['Area Name'], df.iloc[1]['Area Name'])

    def test_numeric_values_format(self):
        """Test that numeric health index values are present and formatted correctly."""
        df = load_csv_data(self.filename)
        
        # Check that year columns have numeric values
        year_columns = ['2015', '2016', '2017', '2018', '2019', '2020', '2021']
        for year in year_columns:
            self.assertIn(year, df.columns)
            # Check first row value is numeric
            self.assertTrue(pd.api.types.is_numeric_dtype(df[year]) or 
                          not pd.isna(pd.to_numeric(df[year].iloc[0], errors='coerce')),
                          f"Column {year} should contain numeric values")

    def test_area_types_present(self):
        """Test that Area Type field contains valid values."""
        df = load_csv_data(self.filename)
        
        # Check first few rows have Area Type
        self.assertIn('Area Type', df.columns)
        self.assertFalse(df['Area Type'].head(5).isna().any(), 
                        "Area Type should not have null values in first 5 rows")
        self.assertTrue((df['Area Type'].head(5).str.len() > 0).all(),
                       "Area Type should not be empty")

    def test_no_empty_area_codes(self):
        """Test that Area Code is not empty for any row."""
        df = load_csv_data(self.filename)
        
        self.assertIn('Area Code', df.columns)
        self.assertFalse(df['Area Code'].head(20).isna().any(),
                        "Area Code should not have null values in first 20 rows")
        self.assertTrue((df['Area Code'].head(20).str.len() > 0).all(),
                       "Area Code should not be empty")

    def test_specific_regions_exist(self):
        """Test that known regions are present in the data."""
        df = load_csv_data(self.filename)
        area_names = df['Area Name'].tolist()
        
        # Check for some known regions
        self.assertIn('ENGLAND', area_names)
        self.assertIn('North East', area_names)
        self.assertIn('North West', area_names)

if __name__ == '__main__':
    unittest.main()
