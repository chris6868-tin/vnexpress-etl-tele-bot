# Define your item pipelines here
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

class PostgresPipeline:
    def open_spider(self, spider):
        self.conn = psycopg2.connect(
            host=os.getenv("DB_HOST", "localhost"),
            port=os.getenv("DB_PORT", "5432"),
            database=os.getenv("DB_NAME", "news_bot_db"),
            user=os.getenv("DB_USER", "admin"),
            password=os.getenv("DB_PASSWORD", "postgres16")
        )

        self.cur = self.conn.cursor()

        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS articles(
                         id SERIAL PRIMARY KEY,
                         title TEXT,
                         url TEXT UNIQUE,
                         content TEXT,
                         created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                         )
        """)
        self.conn.commit()

    def process_item(self, item, spider):
        try:
            self.cur.execute(
                "INSERT INTO articles (title, url, content) VALUES (%s, %s, %s) ON CONFLICT (url) DO NOTHING",
                (item['title'], item['url'], item['content'])
            )
            self.conn.commit()
        except Exception as e:
            spider.logger.error(f"Loi luu DB: {e}")
        return item
    
    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()

# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
