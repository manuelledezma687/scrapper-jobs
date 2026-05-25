import os
import asyncio

from dotenv import load_dotenv
from telegram import Bot

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")

CHAT_IDS = [
    os.getenv("CHAT_ID_1"),
    os.getenv("CHAT_ID_2"),
    os.getenv("CHAT_ID_3"),
]

MAX_MESSAGE_LENGTH = 4000


async def send_chunk(
    bot,
    chat_id,
    text
):

    await bot.send_message(
        chat_id=chat_id,
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

    for chat_id in CHAT_IDS:

        if not chat_id:
            continue

        for chunk in chunks:

            try:

                await send_chunk(
                    bot,
                    chat_id,
                    chunk
                )

            except Exception as e:

                print(
                    f"Telegram Error ({chat_id}): {e}"
                )


def send_telegram_message(message):

    asyncio.run(
        send_message_async(message)
    )