import os
import asyncio

from dotenv import load_dotenv
from telegram import Bot

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

MAX_MESSAGE_LENGTH = 4000


async def send_chunk(bot, text):

    await bot.send_message(
        chat_id=CHAT_ID,
        text=text
    )


async def send_message_async(message):

    bot = Bot(token=TOKEN)

    chunks = []

    while len(message) > MAX_MESSAGE_LENGTH:

        split_index = message.rfind(
            "\n",
            0,
            MAX_MESSAGE_LENGTH
        )

        if split_index == -1:
            split_index = MAX_MESSAGE_LENGTH

        chunks.append(message[:split_index])

        message = message[split_index:]

    chunks.append(message)

    for chunk in chunks:

        await send_chunk(bot, chunk)


def send_telegram_message(message):

    asyncio.run(send_message_async(message))