import unittest
import pandas as pd
import sys
import os

# Add 'src' to the python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

# Importing functions
from data_analysis import filter_data, calculate_stats

class TestDataAnalysis(unittest.TestCase):
    
    def setUp(self):
        """Create a mock DataFrame for analysis."""
        data = {
            'Area Name': ['North', 'South', 'East'],
            'Area Type': ['Region', 'Region', 'LTLA'],
            '2021': [100.0, 150.0, 50.0],
            '2020': [90.0, 140.0, 40.0]
        }
        self.df = pd.DataFrame(data)

    def test_filter_data_by_type(self):
        """Test filtering by Area Type."""
        # want only 'Region' rows
        result = filter_data(self.df, column='Area Type', value='Region')
        
        self.assertEqual(len(result), 2) # Should be North and South
        self.assertTrue(all(result['Area Type'] == 'Region'))

    def test_calculate_stats(self):
        """Test mean, min, and max calculations for a specific column."""
        stats = calculate_stats(self.df, column='2021')
        
        self.assertEqual(stats['mean'], 100.0) # (100+150+50)/3 = 100
        self.assertEqual(stats['min'], 50.0)
        self.assertEqual(stats['max'], 150.0)

    def test_calculate_stats_invalid_column(self):
        """Test that it handles invalid columns gracefully."""
        # Using assertRaises or returning None is fine. expect None or empty dict.
        stats = calculate_stats(self.df, column='GhostYear')
        self.assertIsNone(stats)

    def test_filter_data_empty_dataframe(self):
        """Test filtering an empty DataFrame."""
        empty_df = pd.DataFrame()
        result = filter_data(empty_df, column='Area Type', value='Region')
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(len(result), 0)

    def test_filter_data_no_matches(self):
        """Test filtering with value that doesn't exist."""
        result = filter_data(self.df, column='Area Type', value='NonExistent')
        self.assertEqual(len(result), 0)
        self.assertIsInstance(result, pd.DataFrame)

    def test_filter_data_all_matches(self):
        """Test filtering where all rows match."""
        # Create df where all have same type
        data = {
            'Area Name': ['A', 'B', 'C'],
            'Area Type': ['Region', 'Region', 'Region'],
            '2021': [100.0, 150.0, 50.0]
        }
        df = pd.DataFrame(data)
        result = filter_data(df, column='Area Type', value='Region')
        self.assertEqual(len(result), 3)

    def test_filter_data_invalid_column(self):
        """Test filtering on non-existent column."""
        result = filter_data(self.df, column='FakeColumn', value='Test')
        # should return empty or None - expect empty DataFrame
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(len(result), 0)

    def test_filter_data_preserves_structure(self):
        """Test that filtering preserves DataFrame structure."""
        result = filter_data(self.df, column='Area Type', value='Region')
        # Should have same columns as original
        self.assertEqual(list(result.columns), list(self.df.columns))

    def test_calculate_stats_all_same_values(self):
        """Test stats when all values are identical."""
        data = {
            'Area Name': ['A', 'B', 'C'],
            '2021': [100.0, 100.0, 100.0]
        }
        df = pd.DataFrame(data)
        stats = calculate_stats(df, column='2021')
        
        self.assertEqual(stats['mean'], 100.0)
        self.assertEqual(stats['min'], 100.0)
        self.assertEqual(stats['max'], 100.0)

    def test_calculate_stats_negative_numbers(self):
        """Test stats calculation with negative values."""
        data = {
            'Area Name': ['A', 'B', 'C'],
            '2021': [-50.0, 0.0, 50.0]
        }
        df = pd.DataFrame(data)
        stats = calculate_stats(df, column='2021')
        
        self.assertEqual(stats['mean'], 0.0)
        self.assertEqual(stats['min'], -50.0)
        self.assertEqual(stats['max'], 50.0)

    def test_calculate_stats_single_row(self):
        """Test stats with only one row."""
        data = {
            'Area Name': ['A'],
            '2021': [100.0]
        }
        df = pd.DataFrame(data)
        stats = calculate_stats(df, column='2021')
        
        self.assertEqual(stats['mean'], 100.0)
        self.assertEqual(stats['min'], 100.0)
        self.assertEqual(stats['max'], 100.0)

    def test_calculate_stats_empty_dataframe(self):
        """Test stats calculation on empty DataFrame."""
        empty_df = pd.DataFrame()
        stats = calculate_stats(empty_df, column='2021')
        self.assertIsNone(stats)

    def test_calculate_stats_return_type(self):
        """Test that stats returns a dictionary with expected keys."""
        stats = calculate_stats(self.df, column='2021')
        
        self.assertIsInstance(stats, dict)
        self.assertIn('mean', stats)
        self.assertIn('min', stats)
        self.assertIn('max', stats)

    def test_calculate_stats_with_zeros(self):
        """Test stats calculation with zero values."""
        data = {
            'Area Name': ['A', 'B', 'C'],
            '2021': [0.0, 100.0, 200.0]
        }
        df = pd.DataFrame(data)
        stats = calculate_stats(df, column='2021')
        
        self.assertEqual(stats['mean'], 100.0)
        self.assertEqual(stats['min'], 0.0)
        self.assertEqual(stats['max'], 200.0)

    def test_integration_filter_then_calculate(self):
        """Integration test: filter data then calculate stats."""
        filtered = filter_data(self.df, column='Area Type', value='Region')
        stats = calculate_stats(filtered, column='2021')
        
        # Only North (100) and South (150) are Regions
        self.assertEqual(stats['mean'], 125.0)  # (100+150)/2
        self.assertEqual(stats['min'], 100.0)
        self.assertEqual(stats['max'], 150.0)

    def test_filter_data_case_sensitivity(self):
        """Test that filtering is case-insensitive."""
        result = filter_data(self.df, column='Area Type', value='region')  # lowercase
        # Should match 'Region' (case-insensitive)
        self.assertEqual(len(result), 2)
        self.assertTrue(all(result['Area Type'] == 'Region'))

    def test_filter_data_mixed_case(self):
        """Test case-insensitive filtering with mixed case input."""
        result = filter_data(self.df, column='Area Type', value='rEgIoN')  # mixed case
        # Should still match 'Region'
        self.assertEqual(len(result), 2)

    def test_filter_data_case_insensitive_area_name(self):
        """Test case-insensitive filtering on Area Name column."""
        data = {
            'Area Name': ['London', 'LONDON', 'london', 'LoNdOn', 'Manchester'],
            'Area Type': ['LTLA', 'LTLA', 'LTLA', 'LTLA', 'LTLA'],
            '2021': [100.0, 110.0, 105.0, 108.0, 90.0]
        }
        df = pd.DataFrame(data)
        result = filter_data(df, column='Area Name', value='london')
        
        # Should match all variations of London
        self.assertEqual(len(result), 4)
        # All matched values should be some case variation of 'london'
        for name in result['Area Name']:
            self.assertEqual(name.lower(), 'london')

    def test_calculate_stats_large_numbers(self):
        """Test stats with very large numbers."""
        data = {
            'Area Name': ['A', 'B', 'C'],
            '2021': [1e10, 2e10, 3e10]
        }
        df = pd.DataFrame(data)
        stats = calculate_stats(df, column='2021')
        
        self.assertEqual(stats['mean'], 2e10)
        self.assertEqual(stats['min'], 1e10)
        self.assertEqual(stats['max'], 3e10)

if __name__ == '__main__':
    unittest.main()