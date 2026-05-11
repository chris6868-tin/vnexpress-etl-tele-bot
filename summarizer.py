import os
import psycopg2
from google import genai
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        database=os.getenv("DB_NAME", "news_bot_db"),
        user=os.getenv("DB_USER", "admin"),
        password=os.getenv("DB_PASSWORD", "postgres16")
    )


def AI_work(title, content, url):
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    prompt = f"""
        Bạn là một chuyên gia phân tích tin tức.
        Dựa trên nội dung bài báo dưới đây, hãy tóm tắt trong 3 câu duy nhất.
        Yêu cầu: Khách quan, tập trung vào số liệu hoặc sự kiện quan trọng nhất.

        Nội dung: 
        Tiêu đề: {title}
        Chi tiết: {content[:3000]}
        """

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        summary = response.text.strip()
        if summary:
            return (
                f"📰 *{title}*\n\n"
                f"✨ *Tóm tắt:* {summary}\n\n"
                f"🔗 [Đọc bài gốc]({url})"
            )
    except Exception as e:
        print(f"Loi API tai bai '{title}': {e}")


def summarizer_from_db(limit=5):
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute(
            "SELECT id, title, content, url FROM articles WHERE is_sent = FALSE ORDER BY created_at DESC LIMIT %s",
            (limit,)
        )
        rows = cur.fetchall()

        if not rows:
            print("Khong co du lieu trong db")
        else:
            print(f"Dang xu ly {len(rows)} bai viet... \n")
            for row in rows:
                article_id, title, content, url = row
                message = AI_work(title, content, url)
                if message:
                    yield message
                    cur.execute(
                        "UPDATE articles SET is_sent = TRUE WHERE id = %s",
                        (article_id,)
                    )
                    conn.commit()
                else:
                    print(f"AI khong the tom tat! quy tac: {title}")

        cur.close()
        conn.close()
    except Exception as e:
        print(f"Loi database: {e}")


if __name__ == "__main__":
    for item in summarizer_from_db():
        print(item)

