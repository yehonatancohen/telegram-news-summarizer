import logging
import logging.config
import os

# Load the logging configuration
LOG_CONFIG_PATH = os.path.join(os.path.dirname(__file__), '../../config/logging.conf')
logging.getLogger('telethon.crypto.libssl').setLevel(logging.CRITICAL)
logging.getLogger('telethon.crypto.aes').setLevel(logging.CRITICAL)
logging.config.fileConfig(LOG_CONFIG_PATH)

# Create a logger that can be imported in other modules
logger = logging.getLogger(__name__)