import os
import sys
from pathlib import Path

# Thêm đường dẫn này để Python tìm thấy package picture_solver
sys.path.append(str(Path(__file__).parent))

# Import MaskClassifier từ đúng vị trí thư mục
from picture_solver.digit_classifier.mask_classifier import MaskClassifier

def run_system_test():
    # 1. Xác định đường dẫn đến dữ liệu dựa trên sơ đồ của bạn
    # Thư mục gốc -> res -> digits_00
    base_path = Path(__file__).parent
    data_path = base_path / "res" / "digits_00"
    
    print(f"--- Kiểm tra đường dẫn dữ liệu ---")
    if not data_path.exists():
        print(f"❌ Không tìm thấy thư mục: {data_path}")
        print("Hãy đảm bảo bạn đã tạo thư mục 'digits_00' bên trong 'res'.")
        return
    else:
        print(f"✅ Đã tìm thấy dữ liệu tại: {data_path}")

    # 2. Khởi tạo và chạy test
    print("\n--- Khởi tạo MaskClassifier ---")
    # Máy sẽ quét res/digits_00/0...9 để tạo mask
    # Mask sẽ được lưu tại res/digits_00/masks/
    try:
        model = MaskClassifier(digits_path=str(data_path))
        
        print("\n--- Bắt đầu chấm điểm nhận diện ---")
        model.test(root_path=str(data_path), full_log=True)
        
    except Exception as e:
        print(f"❌ Có lỗi xảy ra: {e}")

if __name__ == "__main__":
    run_system_test()