from utils import logger
from telegram import Telegram
import asyncio, sys, os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from config import get_env_variable

async def main():
    logger.disabled = False
    logger.info("Starting tasks...")

    # Get the API ID and API hash from the environment variables
    api_id = get_env_variable("API_ID")
    api_hash = get_env_variable("API_HASH")
    phone_number = get_env_variable("PHONE_NUMBER")
    password = get_env_variable("PASSWORD")

    # Create a Telegram client and connect to the Telegram API
    telegram = Telegram(api_id=api_id, api_hash=api_hash)
    await telegram.connect(phone_number, password)

    # Join channels
    channel_ids = get_env_variable("CHANNEL_IDS").split(",")
    for channel_id in channel_ids:
        await telegram.join_channel(channel_id)

    # Listen to incoming messages
    await telegram.listen_messages()
    
if __name__ == "__main__":
    asyncio.run(main())