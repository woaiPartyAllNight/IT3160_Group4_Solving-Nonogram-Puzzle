# nonogram_reader.py
import os
import json
import sys
from pathlib import Path
import google.generativeai as genai
from dotenv import load_dotenv

def read_nonogram(image_path: str, output_path: str = None):
    """
    Đọc bảng nonogram từ ảnh và ghi ra input.txt
    
    Args:
        image_path: đường dẫn ảnh đầu vào
        output_path: đường dẫn file output (mặc định: input.txt cạnh ảnh)
    """
    image_path = Path(image_path)
    if output_path is None:
        output_path = image_path.parent / "input.txt"
    
    # Đọc ảnh (Gemini dùng bytes trực tiếp)
    with open(image_path, "rb") as f:
        img_data = f.read()
    
    ext = image_path.suffix.lower()
    media_type_map = {
        ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
        ".png": "image/png", ".webp": "image/webp"
    }
    media_type = media_type_map.get(ext, "image/jpeg")
    
    # Gọi Gemini Vision
    load_dotenv()
    genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
    model = genai.GenerativeModel('gemini-1.5-pro')
    
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
}

Ví dụ với bảng 3x3:
{
  "m": 3,
  "n": 3,
  "row_clues": [[1], [2], [1,1]],
  "col_clues": [[2], [1], [1,1]]
}"""

    response = model.generate_content([
        prompt,
        {"mime_type": media_type, "data": img_data}
    ])
    
    # Parse JSON từ response
    response_text = response.text.strip()
    
    # Xử lý trường hợp response bọc trong markdown code block
    if response_text.startswith("```"):
        lines = response_text.split("\n")
        response_text = "\n".join(lines[1:-1])
    
    data = json.loads(response_text)
    
    m = data["m"]
    n = data["n"]
    row_clues = data["row_clues"]
    col_clues = data["col_clues"]
    
    # Validate
    if len(row_clues) != m:
        raise ValueError(f"row_clues có {len(row_clues)} hàng, kỳ vọng {m}")
    if len(col_clues) != n:
        raise ValueError(f"col_clues có {len(col_clues)} cột, kỳ vọng {n}")
    
    sum_rows = sum(sum(r) for r in row_clues)
    sum_cols = sum(sum(c) for c in col_clues)
    if sum_rows != sum_cols:
        print(f"⚠️  Cảnh báo: tổng hàng ({sum_rows}) ≠ tổng cột ({sum_cols}) — có thể đọc sai")
    
    # Ghi file
    output_path = Path(output_path)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(f"{m} {n}\n")
        for row in row_clues:
            f.write(" ".join(str(x) for x in row) + "\n")
        for col in col_clues:
            f.write(" ".join(str(x) for x in col) + "\n")
    
    print(f"✅ Đã ghi: {output_path}")
    print(f"   Bảng: {m}x{n}")
    print(f"   Tổng ô tô màu: {sum_rows}")
    return output_path


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Dùng: python nonogram_reader.py <ảnh> [output.txt]")
        sys.exit(1)
    
    image = sys.argv[1]
    output = sys.argv[2] if len(sys.argv) > 2 else None
    read_nonogram(image, output)