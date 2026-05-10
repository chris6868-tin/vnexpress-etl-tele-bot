from summarizer import summarizer_from_db


def main():
    print("Chạy tóm tắt bài viết từ cơ sở dữ liệu")
    for message in summarizer_from_db():
        print(message)
        print("\n" + "-" * 80 + "\n")


if __name__ == "__main__":
    main()
