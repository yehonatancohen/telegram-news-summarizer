import logging
import logging.config
import os

logger = None

def init_logger():
    global logger
    if (logger):
        return logger
    # Load the logging configuration
    LOG_CONFIG_PATH = os.path.join(os.path.dirname(__file__), '../../config/logging.conf')
    logging.getLogger('telethon.crypto.libssl').setLevel(logging.CRITICAL)
    logging.getLogger('telethon.crypto.aes').setLevel(logging.CRITICAL)
    logging.config.fileConfig(LOG_CONFIG_PATH)

    # Initialize the logger
    _logger = logging.getLogger(__name__)
    
    # Logger disabled by default
    _logger.disabled = False

    return _logger

# Create a logger that can be imported in other modules
logger = init_logger()
