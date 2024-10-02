from utils import logger
from telegram import Telegram
from db import init_channels, add_telegram_channel, get_telegram_channels
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

    # Initialize the database
    init_channels()

    arab_channels = [
        '@a7rarjenin',
        '@QudsN',
        '@Electrohizbullah',
        '@SerajSat',
        '@shadysopoh',
        '@jeninqassam',
        '@Janin324',
        '@jenin4',
        '@anas_hoshia',
        '@abohamzahasanat',
        '@sarayajneen',
        '@abohamzahasanat',
        '@C_Military1',
        '@mmirleb',
        '@SabrenNews22',
        '@IraninArabic',
        '@iraninarabic_ir',
        '@meshheek',
        '@qassam1brigades',
        '@qassambrigades',
        '@duyuf1',
        '@Ail_2_9',
        '@alghalebun3',
        '@areennabluss'
    ]

    smart_channels = [
        '@abualiexpress',
        '@arabworld301',
        '@AlealamAlearabiuEranMalca',
        '@AsrarLubnan'
    ]


    # Join the channels
    channels = [{'id': channel, 'name': 'Arab', 'reliability': 1} for channel in arab_channels]
    channels += [{'id': channel, 'name': 'Smart', 'reliability': 2} for channel in smart_channels]

    await telegram.join_channels(channels)

    # Listen to incoming messages
    await telegram.listen_messages()
    
if __name__ == "__main__":
    asyncio.run(main())