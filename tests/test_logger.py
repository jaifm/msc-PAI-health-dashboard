import unittest
import os
import sys
import logging
import tempfile
import shutil

# Add 'src' to the python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from activity_logger import setup_logger, log_operation

class TestActivityLogger(unittest.TestCase):
    
    def setUp(self):
        """Create a temporary directory for log files."""
        self.test_dir = tempfile.mkdtemp()
        self.log_file = os.path.join(self.test_dir, 'test_activity.log')
        
        # Clear any existing handlers
        logger = logging.getLogger('HealthDashboard')
        logger.handlers.clear()
    
    def tearDown(self):
        """Clean up temporary directory and log files."""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
        
        # Clear handlers
        logger = logging.getLogger('HealthDashboard')
        logger.handlers.clear()
    
    def test_setup_logger_creates_file(self):
        """Test that setup_logger creates a log file."""
        logger = setup_logger(log_file=self.log_file)
        
        self.assertIsInstance(logger, logging.Logger)
        self.assertTrue(os.path.exists(self.log_file))
    
    def test_log_operation_writes_to_file(self):
        """Test that log_operation writes to the log file."""
        logger = setup_logger(log_file=self.log_file)
        log_operation(logger, "LOAD", "data.csv")
        
        # Read log file
        with open(self.log_file, 'r') as f:
            content = f.read()
        
        self.assertIn("LOAD", content)
        self.assertIn("data.csv", content)
    
    def test_log_operation_with_details(self):
        """Test log_operation with additional details."""
        logger = setup_logger(log_file=self.log_file)
        log_operation(logger, "SAVE", "health.db", details="342 rows saved")
        
        with open(self.log_file, 'r') as f:
            content = f.read()
        
        self.assertIn("SAVE", content)
        self.assertIn("health.db", content)
        self.assertIn("342 rows saved", content)
    
    def test_multiple_log_entries(self):
        """Test multiple log entries in sequence."""
        logger = setup_logger(log_file=self.log_file)
        
        log_operation(logger, "LOAD", "data.csv")
        log_operation(logger, "CLEAN", "data.csv", details="Removed NaN values")
        log_operation(logger, "SAVE", "health.db")
        
        with open(self.log_file, 'r') as f:
            content = f.read()
        
        self.assertIn("LOAD", content)
        self.assertIn("CLEAN", content)
        self.assertIn("SAVE", content)
    
    def test_log_file_has_timestamp(self):
        """Test that log entries have timestamps."""
        logger = setup_logger(log_file=self.log_file)
        log_operation(logger, "TEST", "test.csv")
        
        with open(self.log_file, 'r') as f:
            content = f.read()
        
        # Should contain a timestamp pattern
        import re
        timestamp_pattern = r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}'
        self.assertIsNotNone(re.search(timestamp_pattern, content))

if __name__ == '__main__':
    unittest.main()
