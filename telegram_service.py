# import os
# import json
# import asyncio

# from dotenv import load_dotenv
# from telegram import Update, Bot
# from telegram.ext import (
#     ApplicationBuilder,
#     CommandHandler,
#     ContextTypes
# )

# load_dotenv()

# TOKEN = os.getenv("TELEGRAM_TOKEN")

# SUBSCRIBERS_FILE = "subscribers.json"

# MAX_MESSAGE_LENGTH = 4000


# # ============================================
# # LOAD SUBSCRIBERS
# # ============================================

# def load_subscribers():

#     try:

#         with open(
#             SUBSCRIBERS_FILE,
#             "r"
#         ) as file:

#             return json.load(file)

#     except:

#         return []


# # ============================================
# # SAVE SUBSCRIBERS
# # ============================================

# def save_subscribers(subscribers):

#     with open(
#         SUBSCRIBERS_FILE,
#         "w"
#     ) as file:

#         json.dump(subscribers, file)


# # ============================================
# # /START COMMAND
# # ============================================

# async def start(
#     update: Update,
#     context: ContextTypes.DEFAULT_TYPE
# ):

#     chat_id = update.effective_chat.id

#     subscribers = load_subscribers()

#     if chat_id not in subscribers:

#         subscribers.append(chat_id)

#         save_subscribers(subscribers)

#     await update.message.reply_text(
#         "✅ Subscribed to QA Jobs Alerts"
#     )


# # ============================================
# # START BOT LISTENER
# # ============================================

# def run_bot():

#     app = (
#         ApplicationBuilder()
#         .token(TOKEN)
#         .build()
#     )

#     app.add_handler(
#         CommandHandler("start", start)
#     )

#     print("Telegram bot running...")

#     app.run_polling()


# # ============================================
# # SEND MESSAGE TO ALL
# # ============================================

# async def send_chunk(
#     bot,
#     chat_id,
#     text
# ):

#     await bot.send_message(
#         chat_id=chat_id,
#         text=text
#     )


# async def send_message_async(message):

#     bot = Bot(token=TOKEN)

#     subscribers = load_subscribers()

#     chunks = []

#     while len(message) > MAX_MESSAGE_LENGTH:

#         split_index = message.rfind(
#             "\n",
#             0,
#             MAX_MESSAGE_LENGTH
#         )

#         if split_index == -1:
#             split_index = MAX_MESSAGE_LENGTH

#         chunks.append(message[:split_index])

#         message = message[split_index:]

#     chunks.append(message)

#     for subscriber in subscribers:

#         for chunk in chunks:

#             try:

#                 await send_chunk(
#                     bot,
#                     subscriber,
#                     chunk
#                 )

#             except Exception as e:

#                 print(
#                     f"Telegram Error: {e}"
#                 )


# def send_telegram_message(message):

#     asyncio.run(
#         send_message_async(message)
#     )

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