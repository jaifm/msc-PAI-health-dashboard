import logging
import os

def setup_logger(log_file='logs/activity.log'):
    """
    Sets up a logger that writes to a file with timestamps.
    
    Args:
        log_file (str): Path to the log file.
        
    Returns:
        logging.Logger: Configured logger instance.
    """
    # Create logs directory if it doesn't exist
    log_dir = os.path.dirname(log_file)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Create logger
    logger = logging.getLogger('HealthDashboard')
    logger.setLevel(logging.INFO)
    
    # Avoid adding handlers multiple times
    if logger.handlers:
        return logger
    
    # Create formatter with timestamp
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # File handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    
    # Add handler to logger
    logger.addHandler(file_handler)
    
    return logger

def log_operation(logger, operation, filename, details=None):
    """
    Logs a data operation with optional details.
    
    Args:
        logger: Logger instance.
        operation (str): Type of operation (e.g., 'LOAD', 'SAVE', 'CLEAN').
        filename (str): File or database name.
        details (str, optional): Additional details about the operation.
    """
    msg = f"[{operation}] {filename}"
    if details:
        msg += f" - {details}"
    logger.info(msg)
