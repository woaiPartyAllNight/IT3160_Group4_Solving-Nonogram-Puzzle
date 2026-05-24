import os
import json
import time
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel

class NonogramSchema(BaseModel):
    m: int
    n: int
    row_clues: list[list[int]]
    col_clues: list[list[int]]

# Ẩn cảnh báo hệ thống của gRPC
os.environ["GRPC_VERBOSITY"] = "NONE"
os.environ["GLOG_minloglevel"] = "2"


PROMPT = """
Bạn hãy đọc ảnh bảng Nonogram và trả về JSON đúng định dạng sau:
{
  "m": <số hàng>,
  "n": <số cột>,
  "row_clues": [[...], [...]],
  "col_clues": [[...], [...]]
}

Quy tắc:
- row_clues là các gợi ý bên trái bảng, đọc từ trên xuống dưới.
- col_clues là các gợi ý phía trên bảng, đọc từ trái sang phải.
- Trong mỗi hàng/cột clue, đọc số theo đúng thứ tự xuất hiện.
- Nếu hàng/cột không có số gợi ý, dùng [].
- Chỉ trả về JSON, không giải thích thêm.
"""


def normalize_clues(clues):
    """Chuẩn hóa clue từ Gemini về dạng list[list[int]]."""
    result = []
    for line in clues:
        if line == [] or line == [0] or line == ["0"]:
            result.append([])
        else:
            result.append([int(x) for x in line])
    return result


def validate_puzzle(m, n, row_clues, col_clues):
    """Kiểm tra nhanh dữ liệu trước khi đưa vào solver."""
    if len(row_clues) != m:
        raise ValueError(f"Sai số hàng: m={m}, nhưng có {len(row_clues)} row clues")

    if len(col_clues) != n:
        raise ValueError(f"Sai số cột: n={n}, nhưng có {len(col_clues)} col clues")


    for i, row in enumerate(row_clues):
        if row and sum(row) + len(row) - 1 > n:
            raise ValueError(f"Row {i + 1} không hợp lệ: {row}")

    for j, col in enumerate(col_clues):
        if col and sum(col) + len(col) - 1 > m:
            raise ValueError(f"Col {j + 1} không hợp lệ: {col}")


def write_input_file(output_path, m, n, row_clues, col_clues):
    """Ghi dữ liệu ra file txt theo format input của solver."""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(f"{m} {n}\n")

        for row in row_clues:
            f.write((" ".join(map(str, row)) if row else "0") + "\n")

        for col in col_clues:
            f.write((" ".join(map(str, col)) if col else "0") + "\n")


def process_image(image_path: str, save_txt: bool = False, output_path: str = None):
    """
    Demo nhận diện ảnh Nonogram bằng Gemini.

    Đầu vào:
        image_path: đường dẫn ảnh Nonogram
        save_txt: có lưu ra file input txt hay không
        output_path: đường dẫn file text output (nếu save_txt=True)

    Đầu ra:
        m, n, row_clues, col_clues
    """
    image_path = Path(image_path)
    if not image_path.exists():
        raise FileNotFoundError(f"Không tìm thấy ảnh tại {image_path}")

    media_type_map = {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".webp": "image/webp",
    }
    media_type = media_type_map.get(image_path.suffix.lower())
    if media_type is None:
        raise ValueError("Chỉ hỗ trợ ảnh .jpg, .jpeg, .png, .webp")

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("Chưa thiết lập GEMINI_API_KEY trong file .env hoặc biến môi trường")

    client = genai.Client(api_key=api_key)
    img_data = image_path.read_bytes()

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[
            types.Part.from_bytes(data=img_data, mime_type=media_type),
            PROMPT,
        ],
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=NonogramSchema,
            temperature=0,
        ),
    )

    try:
        data = json.loads(response.text)
    except json.JSONDecodeError:
        raise RuntimeError(f"Gemini không trả về JSON hợp lệ:\n{response.text}")

    m = int(data["m"])
    n = int(data["n"])
    row_clues = normalize_clues(data["row_clues"])
    col_clues = normalize_clues(data["col_clues"])

    validate_puzzle(m, n, row_clues, col_clues)

    if save_txt:
        if output_path:
            output_txt = Path(output_path)
        else:
            output_txt = image_path.parent / f"{image_path.stem}_input.txt"
        write_input_file(output_txt, m, n, row_clues, col_clues)
        print(f"[+] Đã lưu file input tại: {output_txt}")

    return m, n, row_clues, col_clues


if __name__ == "__main__":
    import sys

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    # picture_detector.py nằm trong src/api_picture/
    project_root = Path(__file__).resolve().parent.parent.parent
    test_dir = project_root / "test"
    result_dir = project_root / "result"

    if not result_dir.exists():
        result_dir.mkdir(parents=True)

    print(f"[*] Đang quét thư mục: {test_dir}")
    
    valid_exts = {".jpg", ".jpeg", ".png", ".webp"}
    
    for img_path in test_dir.rglob("*"):
        if img_path.is_file() and img_path.suffix.lower() in valid_exts:
            print(f"\n[*] Đang xử lý ảnh: {img_path}")
            
            # Giữ nguyên cấu trúc thư mục của test
            rel_path = img_path.relative_to(test_dir)
            output_txt_path = result_dir / rel_path.with_suffix(".txt")
            
            # Tạo các thư mục con trong result nếu chưa có
            output_txt_path.parent.mkdir(parents=True, exist_ok=True)
            
            try:
                m, n, row_clues, col_clues = process_image(img_path, save_txt=True, output_path=str(output_txt_path))
                print("[+] Nhận diện thành công")
                print(f"Kích thước: {m}x{n}")
            except Exception as e:
                print(f"[!] Lỗi: {e}")
            
            time.sleep(3)
