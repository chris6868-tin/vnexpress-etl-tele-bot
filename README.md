# NewsBot

NewsBot is a news scraping and summarization system that crawls articles from VnExpress, stores them in PostgreSQL, summarizes them using Google Gemini AI, and sends notifications via Telegram.

## Features

- Scrapes news from `vnexpress.net` using Scrapy
- Saves articles to PostgreSQL
- Generates short summaries with Google Gemini AI
- Sends summary notifications to Telegram
- Provides clear script and CLI entry points

## Requirements

- Python 3.13+
- PostgreSQL
- Telegram bot token
- Telegram chat ID
- Google Gemini API key

## Dependencies

- `google-genai`
- `psycopg2`
- `python-dotenv`
- `python-telegram-bot`
- `scrapy`

## Installation

1. Clone the repository:

```powershell
git clone https://github.com/chris6868-tin/vnexpress-etl-tele-bot.git
cd newsbot
```

2. Create and activate a virtual environment:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

3. Install dependencies:

```powershell
python -m pip install --upgrade pip
python -m pip install google-genai psycopg2 python-dotenv python-telegram-bot scrapy
```

4. If you use `uv` as a command wrapper, run commands through it:

```powershell
uv run python main.py summary
uv run python run_scrape.py
```

## Configuration

Create a `.env` file in the project root with the following values:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=news_bot_db
DB_USER=admin
DB_PASSWORD=postgres16
TELEGRAM_BOT_TOKEN=your-telegram-bot-token
TELEGRAM_CHAT_ID=your-chat-id
GEMINI_API_KEY=your-google-gemini-api-key
```

> If you are using `docker-compose.yml`, make sure `DB_PORT` in `.env` matches the port mapping used by Docker.

## Usage

### Run the Scrapy crawler

```powershell
python run_scrape.py
```

Or:

```powershell
python main.py scrape
```

### Run the summary process

```powershell
python run_summary.py
```

Or:

```powershell
python main.py summary
```

### Send a Telegram test message

```powershell
python run_telegram.py
```

Or:

```powershell
python main.py telegram
```

### Run the full workflow

```powershell
python main.py all
```

## Project structure

- `main.py` - main CLI entry point
- `run_scrape.py` - script to run the Scrapy crawler
- `run_summary.py` - script to summarize articles
- `run_telegram.py` - script to send a Telegram test message
- `databaser.py` - database helper for reading articles
- `summarizer.py` - prompt builder and Gemini AI integration
- `sender.py` - Telegram message sender
- `telebot.py` - Telegram bot example
- `scraper/` - Scrapy project
  - `scraper/spiders/vnexpress.py` - VnExpress spider
  - `scraper/pipelines.py` - PostgreSQL storage pipeline
  - `scraper/settings.py` - Scrapy settings

## Notes

- `scraper/pipelines.py` uses the `DB_PORT` environment variable and defaults to `5432` if absent.
- If PostgreSQL is running in Docker, verify the port mapping in `docker-compose.yml`.
- Make sure `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` are set correctly before sending messages.
- Consider tracking article status (summary/sent) in the database to avoid duplicates.
