import os
import sys
from pathlib import Path

# Thêm thư mục code vào Python path để import các modules khác
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# Khuyến nghị: Hạn chế dùng "import *" để tránh xung đột tên và giúp IDE gợi ý code tốt hơn
from util.nonogram import Nonogram
from nonogram_detector.binarize_fn import binarize_adaptive_threshold, binarize_fixed_threshold
from nonogram_detector.nonogram_detector import NonogramDetector
from nonogram_detector.rectangle_fn import rectangle_approx_poly
from perspective_transformer.perspective_transformer import PerspectiveTransformer
from line_detector.line_detector import LinesDetector
from line_detector.line_detector_fn import lines_nxm_kernel
from digit_detector.digit_detector import DigitDetector
from digit_classifier.mask_classifier import MaskClassifier
from nonogram_solver.nonogram_solver import NonogramSolver
# from solution_creator.solution_creator import SolutionCreator

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    # 1. Quản lý đường dẫn thông minh bằng pathlib (Thay thế cho chuỗi "..\\..\\res\\")
    # Lấy thư mục hiện tại chứa file main.py
    current_dir = Path(__file__).resolve().parent
    
    # Giả sử thư mục res nằm ở gốc dự án (lùi ra ngoài các cấp tương ứng)
    base_path = current_dir.parent.parent / "res"
    
    # folder_name, ext = "p7_l10", "jpg"
    # folder_name, ext = "iphone5s", "JPG"
    folder_name, ext = "i8750", "jpg"

    # Đường dẫn test và result
    test_path = base_path / "test" / folder_name
    result_path = base_path / "result" / folder_name
    masks_path = base_path / "digits_00" / "masks"

    # 2. Tạo thư mục result nếu chưa tồn tại (exist_ok=True giúp không báo lỗi nếu đã có)
    result_path.mkdir(parents=True, exist_ok=True)

    # Lấy danh sách toàn bộ ảnh cần xử lý bằng pathlib (Thay thế cho hàm get_files cũ)
    image_files = list(test_path.rglob(f"*.{ext}"))
    
    if not image_files:
        print(f"Cảnh báo: Không tìm thấy file {ext} nào trong {test_path}")
        return

    print(f"🚀 Bắt đầu giải {len(image_files)} câu đố Nonogram...")

    # 3. Vòng lặp xử lý hàng loạt
    for i, image_path in enumerate(image_files):
        print(f"\n[{i+1}/{len(image_files)}] Đang xử lý: {image_path.name}")
        
        # Khởi tạo các pipeline components
        nonogram_detector = NonogramDetector(binarize_adaptive_threshold, rectangle_approx_poly)
        transformer = PerspectiveTransformer(binarize_fixed_threshold(200), binarize_adaptive_threshold)
        line_detector = LinesDetector(lines_nxm_kernel)
        classifier = MaskClassifier(masks_path=str(masks_path))
        digit_detector = DigitDetector(classifier)
        nonogram_solver = NonogramSolver()
        # solution_creator = SolutionCreator()

        # Gọi Facade Nonogram
        solver = Nonogram(
            image=str(image_path), 
            nonogram_detector=nonogram_detector, 
            perspective_transformer=transformer,
            line_detector=line_detector, 
            digit_detector=digit_detector,
            digit_classifier=classifier, 
            nonogram_solver=nonogram_solver,
            # solution_creator=solution_creator
        )
        
        # 4. Bọc Try/Except để lỗi 1 ảnh không làm sập toàn bộ tiến trình
        try:
            solver.solve()
            print(f"✅ Đã giải xong {image_path.name}")
        except Exception as e:
            import traceback
            traceback.print_exc()
            print(f"❌ Lỗi khi giải {image_path.name}: {e}")

if __name__ == "__main__":
    main()