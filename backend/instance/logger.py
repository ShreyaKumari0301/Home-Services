import logging

# Set up logging
logging.basicConfig(
    filename='app.log',  # Log file path
    level=logging.INFO,  # Minimum log level (INFO, DEBUG, ERROR, etc.)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Create a custom logger
logger = logging.getLogger(__name__)