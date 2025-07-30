import argparse
import logging
from pathlib import Path
from zipvoice.tokenizer.tokenizer import EspeakTokenizer


def main():
    """
    Hàm chính để chuyển đổi một câu văn bản thành chuỗi phoneme ID.
    """
    parser = argparse.ArgumentParser(
        description="Chuyển đổi văn bản Tiếng Việt sang Phoneme ID bằng EspeakTokenizer."
    )
    parser.add_argument(
        "--token-file",
        type=str,
        required=True,
        help="Đường dẫn đến file tokens.txt."
    )
    parser.add_argument(
        "--lang",
        type=str,
        default="vi",
        help="Mã ngôn ngữ cho espeak-ng. Mặc định là 'vi'."
    )
    parser.add_argument(
        "--text",
        type=str,
        required=True,
        help="Câu văn bản Tiếng Việt cần chuyển đổi."
    )
    args = parser.parse_args()

    token_file_path = Path(args.token_file)
    if not token_file_path.is_file():
        print(f"LỖI: Không tìm thấy file token tại: {args.token_file}")
        return

    print(f"Đang khởi tạo tokenizer cho ngôn ngữ '{args.lang}'...")
    # Khởi tạo tokenizer với ngôn ngữ Tiếng Việt
    try:
        tokenizer = EspeakTokenizer(token_file=args.token_file, lang=args.lang)
    except Exception as e:
        print(f"Lỗi khi khởi tạo EspeakTokenizer: {e}")
        print("Hãy chắc chắn bạn đã cài đặt piper_phonemize và espeak-ng trên hệ thống.")
        return

    print("Đang chuyển đổi văn bản sang phoneme ID...")
    # Phương thức texts_to_token_ids sẽ làm toàn bộ quá trình:
    # Text -> Phonemes (dạng chữ) -> Phoneme IDs (dạng số)
    token_ids_list = tokenizer.texts_to_token_ids([args.text])
    
    # Lấy kết quả cho câu đầu tiên (và duy nhất)
    phoneme_ids = token_ids_list[0]

    print("\n--- KẾT QUẢ ---")
    print(f"Văn bản gốc: {args.text}")
    print(f"Chuỗi Phoneme ID: {phoneme_ids}")
    print("\nSao chép và dán mảng số ở trên vào code React Native của bạn.")


if __name__ == "__main__":
    # Tắt các log không cần thiết từ các thư viện khác
    logging.basicConfig(level=logging.WARNING)
    main()