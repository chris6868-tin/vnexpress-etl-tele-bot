import os
import subprocess
import sys


def run_scrape():
    project_dir = os.path.dirname(os.path.abspath(__file__))
    print("Chạy Scrapy crawler: vnexpress")
    subprocess.run(
        [sys.executable, "-m", "scrapy", "crawl", "vnexpress"],
        check=True,
        cwd=project_dir,
    )


if __name__ == "__main__":
    run_scrape()
