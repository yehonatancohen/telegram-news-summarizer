import logging
import logging.config
import os

# Load the logging configuration
LOG_CONFIG_PATH = os.path.join(os.path.dirname(__file__), '../../config/logging.conf')
logging.config.fileConfig(LOG_CONFIG_PATH)

# Create a logger that can be imported in other modules
logger = logging.getLogger(__name__)