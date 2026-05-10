import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

def get_raw_news():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
    
        cur.execute("SELECT title, url, content FROM articles ORDER BY created_at DESC LIMIT 5")
        rows = cur.fetchall()
        
        if not rows:
            print("Khong co du lieu trong db")
        else:
            print(f"Dang xu ly {len(rows)} bai viet... \n")
            cur.close()
            conn.close()
            return rows
        
        cur.close()
        conn.close()
        
    except Exception as e:
            print("Loi connect database!")