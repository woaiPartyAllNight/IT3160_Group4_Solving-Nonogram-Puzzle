import os
import json
from pathlib import Path
import google.generativeai as genai
from dotenv import load_dotenv

# Ẩn các cảnh báo hệ thống của gRPC
os.environ["GRPC_VERBOSITY"] = "NONE"
os.environ["GLOG_minloglevel"] = "2"

def process_image(image_path: str, save_txt: bool = False):
    """
    Hàm lõi: Nhận diện ảnh Nonogram bằng Gemini.
    Đầu vào: image_path (Đường dẫn ảnh)
    Đầu ra: tuple (m, n, row_clues, col_clues) để nạp thẳng vào Solver
    """
    image_path = Path(image_path)
    if not image_path.exists():
        raise FileNotFoundError(f"Không tìm thấy ảnh tại {image_path}")

    # Đọc byte ảnh
    with open(image_path, "rb") as f:
        img_data = f.read()
    
    ext = image_path.suffix.lower()
    media_type_map = {
        ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
        ".png": "image/png", ".webp": "image/webp"
    }
    media_type = media_type_map.get(ext, "image/jpeg")
    
    # Cấu hình API
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("Chưa thiết lập GEMINI_API_KEY trong môi trường.")

    genai.configure(api_key=api_key)
    # Tối ưu dùng flash để tốc độ phản hồi nhanh hơn
    model = genai.GenerativeModel('gemini-1.5-flash') 
    
    prompt = """Đây là ảnh bảng Nonogram. Hãy đọc các số gợi ý (clues) từ bảng này.

Quy tắc đọc:
- Góc trên bên trái là vùng trống (giao giữa header hàng và header cột)
- Phần TRÊN bảng chơi: gợi ý cho từng CỘT (đọc từ trái sang phải, từng cột đọc từ trên xuống dưới)
- Phần TRÁI bảng chơi: gợi ý cho từng HÀNG (đọc từ trên xuống dưới, từng hàng đọc từ trái sang phải)

Trả về JSON theo đúng format này, không thêm bất kỳ text nào khác:
{
  "m": <số hàng của bảng chơi>,
  "n": <số cột của bảng chơi>,
  "row_clues": [[số, ...], ...],
  "col_clues": [[số, ...], ...]
}"""

    # Gọi API
    response = model.generate_content(
        [prompt, {"mime_type": media_type, "data": img_data}],
        generation_config={"response_mime_type": "application/json"}
    )
    
    try:
        data = json.loads(response.text)
        m = data["m"]
        n = data["n"]
        row_clues = data["row_clues"]
        col_clues = data["col_clues"]
    except json.JSONDecodeError:
        raise RuntimeError(f"Lỗi: Gemini không trả về JSON hợp lệ. Raw text: {response.text}")
    
    # Optional: Lưu ra file input.txt để đối chiếu nếu bạn muốn
    if save_txt:
        output_txt = image_path.parent / f"{image_path.stem}_input.txt"
        with open(output_txt, "w", encoding="utf-8") as f:
            f.write(f"{m} {n}\n")
            for row in row_clues:
                f.write(" ".join(str(x) for x in row) + "\n")
            for col in col_clues:
                f.write(" ".join(str(x) for x in col) + "\n")

    # TRẢ VỀ CHUẨN ĐẦU VÀO CHO SOLVER
    return m, n, row_clues, col_clues