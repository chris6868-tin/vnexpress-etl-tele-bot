import subprocess
import sys


def run_scrape():
    print("Chạy Scrapy crawler: vnexpress")
    subprocess.run([sys.executable, "-m", "scrapy", "crawl", "vnexpress"], check=True)


if __name__ == "__main__":
    run_scrape()
