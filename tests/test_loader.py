import unittest, os, sys

# Adjust the path to import from src directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from data_loader import load_csv_data

class TestDataLoader(unittest.TestCase):
    
    def setUp(self):
        """Runs before each test. Useful for setup."""
        self.filename = "data/overall_health_index.csv"

    def test_load_csv_structure(self):
        """Test that data loads as a list of dictionaries."""
        data = load_csv_data(self.filename)
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0, "Data list should not be empty")
        self.assertIsInstance(data[0], dict, "Rows should be dictionaries")

    def test_load_csv_content(self):
        """Test that specific columns from the health index file exist."""
        data = load_csv_data(self.filename)
        first_row = data[0]
        
        # Check for expected keys
        self.assertIn('Area Name', first_row)
        self.assertIn('Area Code', first_row)
        self.assertIn('2015', first_row) 
        
        # Check if the values match ('ENGLAND' is first)
        self.assertEqual(data[0]['Area Name'], 'ENGLAND')

    def test_file_not_found(self):
        """Test that the loader handles missing files gracefully."""
        with self.assertRaises(FileNotFoundError):
            load_csv_data("data/ghost_file.csv")

    def test_all_expected_columns(self):
        """Test that all expected columns are present."""
        data = load_csv_data(self.filename)
        first_row = data[0]
        
        expected_columns = ['Area Code', 'Area Name', 'Area Type', 
                          '2015', '2016', '2017', '2018', '2019', '2020', '2021']
        for column in expected_columns:
            self.assertIn(column, first_row, f"Column '{column}' should exist")

    def test_multiple_rows_loaded(self):
        """Test that multiple rows are loaded, not just the first."""
        data = load_csv_data(self.filename)
        self.assertGreater(len(data), 10, "Should load more than 10 rows")
        
        # Verify second row is different from first
        self.assertNotEqual(data[0]['Area Name'], data[1]['Area Name'])

    def test_numeric_values_format(self):
        """Test that numeric health index values are present and formatted correctly."""
        data = load_csv_data(self.filename)
        first_row = data[0]
        
        # Check that year columns have values
        for year in ['2015', '2016', '2017', '2018', '2019', '2020', '2021']:
            self.assertIn(year, first_row)
            self.assertIsNotNone(first_row[year])
            # Value should be convertible to float
            try:
                float(first_row[year])
            except ValueError:
                self.fail(f"Value for {year} should be numeric, got: {first_row[year]}")

    def test_area_types_present(self):
        """Test that Area Type field contains valid values."""
        data = load_csv_data(self.filename)
        
        # Check first few rows have Area Type
        for i in range(min(5, len(data))):
            self.assertIn('Area Type', data[i])
            self.assertIsNotNone(data[i]['Area Type'])
            self.assertGreater(len(data[i]['Area Type']), 0, "Area Type should not be empty")

    def test_no_empty_area_codes(self):
        """Test that Area Code is not empty for any row."""
        data = load_csv_data(self.filename)
        
        for i, row in enumerate(data[:20]):  # Check first 20 rows
            self.assertIn('Area Code', row)
            self.assertIsNotNone(row['Area Code'])
            self.assertGreater(len(row['Area Code']), 0, 
                             f"Area Code should not be empty at row {i}")

    def test_specific_regions_exist(self):
        """Test that known regions are present in the data."""
        data = load_csv_data(self.filename)
        area_names = [row['Area Name'] for row in data]
        
        # Check for some known regions
        self.assertIn('ENGLAND', area_names)
        self.assertIn('North East', area_names)
        self.assertIn('North West', area_names)

if __name__ == '__main__':
    unittest.main()
