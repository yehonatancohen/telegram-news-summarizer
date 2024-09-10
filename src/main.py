from .utils import logger
from .telegram import Telegram
import asyncio
from config import get_env_variable

async def main():
    logger.info("Starting tasks...")

    # Get the API ID and API hash from the environment variables
    api_id = get_env_variable("API_ID")
    api_hash = get_env_variable("API_HASH")

    # Create a Telegram client and connect to the Telegram API
    telegram = Telegram(api_id=api_id, api_hash=api_hash)
    telegram.connect()

    # Join channels
    channel_ids = get_env_variable("CHANNEL_IDS").split(",")
    for channel_id in channel_ids:
        telegram.join_channel(channel_id)

    # Listen to incoming messages
    telegram.listen_messages()
    
if __name__ == "__main__":
    asyncio.run(main())