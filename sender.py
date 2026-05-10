import asyncio
import os
from dotenv import load_dotenv
from telegram import Bot
from telegram.constants import ParseMode


load_dotenv()

async def send_to_telegram(message):

    bot = Bot(token=os.getenv("TELEGRAM_BOT_TOKEN"))
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    await bot.send_message(
        chat_id=chat_id,
        text=message,
        parse_mode=ParseMode.MARKDOWN
    )

    print("Da gui Telegram")

    await asyncio.sleep(2)
