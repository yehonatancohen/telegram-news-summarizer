import os
from dotenv import load_dotenv
from src.utils import logger

# Load environment variables from the .env file
load_dotenv()

def get_env_variable(var_name):
    """Helper function to get an environment variable or raise an exception if not found."""
    value = os.getenv(var_name)
    if value is None:
        logger.error(f"Environment variable {var_name} not found.")
        raise Exception(f"Environment variable {var_name} not found.")
    return value
