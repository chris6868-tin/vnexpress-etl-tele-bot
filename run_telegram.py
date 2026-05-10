import asyncio

from sender import send_to_telegram


async def main():
    message = (
        "✅ NewsBot Telegram test message. \n"
        "Bot is configured and ready to send news summaries."
    )
    await send_to_telegram(message)


if __name__ == "__main__":
    asyncio.run(main())
