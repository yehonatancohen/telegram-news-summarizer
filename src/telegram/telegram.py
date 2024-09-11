from telethon.sync import TelegramClient, events
from telethon.tl.functions.channels import JoinChannelRequest, LeaveChannelRequest, GetFullChannelRequest
from telethon.errors import ChannelPrivateError
from utils import logger

class Telegram:
    def __init__(self, api_id, api_hash, session_name="default_session"):
        self.api_id = api_id
        self.api_hash = api_hash
        self.client = TelegramClient(session_name, self.api_id, self.api_hash)
        self.client.add_event_handler(self.handle_message, events.NewMessage)
        

    async def connect(self, phone_number, password=None):
        # Connect to the Telegram API
        await self.client.start(phone_number, password)
        if not await self.client.is_user_authorized():
            logger.info("User not authorized")
        logger.info("Connected to Telegram API")

    def handle_message(self, event):
        # Handle incoming messages
        logger.info("Received message:", event.message.text)

    async def listen_messages(self):
        # Listen to incoming messages
        @self.client.on(events.NewMessage)
        async def handle_message(event):
            logger.info("Received message:", event.message.text)

        await self.client.run_until_disconnected()
        

    async def is_user_in_channel(self, channel_username):
        try:
            channel = await self.client.get_entity(channel_username)

            full_channel = await self.client(GetFullChannelRequest(channel=channel))

            if full_channel.full_chat.participants_count > 0:
                return True
            else:
                return False
        except ChannelPrivateError:
            logger.error(f"The channel {channel_username} is private or not accessible.")
            return False
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            return False

    async def join_channel(self, channel_id):
        # Join a Telegram channel
        # Check if already in channel
        if await self.is_user_in_channel(channel_id):
            logger.info("Already in channel: " + channel_id)
        else:
            await self.client(JoinChannelRequest(channel_id))
            logger.info("Joined channel: " + channel_id)

    async def leave_channel(self, channel_id):
        # Leave a Telegram channel
        await self.client(LeaveChannelRequest(channel_id))
        logger.info("Left channel:", channel_id)