import argparse
import asyncio
import subprocess
import sys

from databaser import get_raw_news
from sender import send_to_telegram
from summarizer import summarizer_from_db


def run_scrape():
    print("Chạy Scrapy crawler: vnexpress")
    subprocess.run([sys.executable, "-m", "scrapy", "crawl", "vnexpress"], check=True)


def run_summary():
    print("Chạy tóm tắt bài viết từ cơ sở dữ liệu")
    for message in summarizer_from_db():
        print(message)
        print("\n" + "-" * 80 + "\n")


async def run_telegram():
    test_message = (
        "✅ NewsBot Telegram test message.\n"
        "Bot is configured and ready to send news summaries."
    )
    await send_to_telegram(test_message)


async def run_all():
    run_scrape()

    messages = []
    for message in summarizer_from_db():
        messages.append(message)
        print(message)
        print("\n" + "-" * 80 + "\n")

    if not messages:
        print("Không có bài viết nào để gửi.")
        return

    for message in messages:
        await send_to_telegram(message)


def main():
    parser = argparse.ArgumentParser(description="NewsBot entry point")
    parser.add_argument(
        "command",
        choices=["scrape", "summary", "telegram", "all"],
        help="Chế độ chạy: scrape, summary, telegram, all"
    )
    args = parser.parse_args()

    if args.command == "scrape":
        run_scrape()
    elif args.command == "summary":
        run_summary()
    elif args.command == "telegram":
        asyncio.run(run_telegram())
    elif args.command == "all":
        asyncio.run(run_all())


if __name__ == "__main__":
    main()
