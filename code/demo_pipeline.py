import cv2
from pathlib import Path

# Import các class từ project của bạn
from nonogram_detector.nonogram_detector import NonogramDetector
from perspective_transformer.perspective_transformer import PerspectiveTransformer
from code.line_detector.line_detector import LinesDetector
from digit_detector.digit_detector import DigitDetector
from digit_classifier.mask_classifier import MaskClassifier

def run_pipeline(image_filename):
    # -------------------------------------------------------------------
    # ĐỊNH TƯỚNG ĐƯỜNG DẪN THƯ MỤC 'res'
    # -------------------------------------------------------------------
    # Lấy đường dẫn của thư mục đang chứa file demo_pipeline.py (thư mục 'code')
    current_code_dir = Path(__file__).resolve().parent
    
    # Lùi ra một cấp để ra thư mục gốc của dự án, sau đó trỏ vào thư mục 'res'
    project_root = current_code_dir.parent
    image_path = project_root / "res" / image_filename

    print(f"[0] Đọc ảnh đầu vào từ: {image_path}")
    
    # Ép kiểu image_path về chuỗi (string) để OpenCV có thể đọc được
    original_image = cv2.imread(str(image_path))
    
    if original_image is None:
        print(f"❌ Lỗi: Không đọc được ảnh! Vui lòng kiểm tra lại xem file '{image_filename}' có tồn tại trong thư mục 'res' không.")
        return

    # =====================================================================
    # (Phần còn lại của code giữ nguyên như cũ)
    # =====================================================================
    
    def my_binarize_fn(img):
        _, binary = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
        return binary
        
    def my_rectangle_fn(contour):
        epsilon = 0.02 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)
        if len(approx) == 4: return approx
        return contour

    def my_line_detection_fn(img):
        edges = cv2.Canny(img, 50, 150)
        return edges, edges 

    print("[1] Khởi chạy NonogramDetector...")
    detector = NonogramDetector(binarize_fn=my_binarize_fn, rectangle_fn=my_rectangle_fn)
    resized_img, binary_img, rects = detector.detect(original_image)

    if not rects:
        print("Lỗi: Không tìm thấy khung lưới nào!")
        return
    largest_contour = max(rects, key=cv2.contourArea)

    print("[2] Khởi chạy PerspectiveTransformer...")
    transformer = PerspectiveTransformer()
    transformer.set_image(resized_img)
    transformer.set_contour(largest_contour)
    warped_img = transformer.get_result()

    print("[3] Khởi chạy LinesDetector...")
    line_detector = LinesDetector(line_detection_fn=my_line_detection_fn)
    line_detector.set_image(warped_img)
    (img_v, img_h), (coords_v, coords_h) = line_detector.get_result()

    coords_v = [int(c) for c in coords_v]
    coords_h = [int(c) for c in coords_h]

    print("[4] Khởi chạy DigitDetector & Classifier...")
    
    # Cập nhật lại đường dẫn tới thư mục masks luôn cho chuẩn xác
    masks_dir = current_code_dir / "digit_classifier" / "masks"
    classifier = MaskClassifier(masks_path=str(masks_dir)) 
    
    digit_detector = DigitDetector(classifier)
    digit_detector.set_image(warped_img)
    digit_detector.set_lines(coords_v, coords_h)
    
    display_img, clues = digit_detector.get_result()

    print("[5] Kết quả dữ liệu đầu vào cho Solver:")
    if clues:
        cols_clues, rows_clues = clues
        print("Gợi ý Cột (col_list):", cols_clues)
        print("Gợi ý Hàng (row_list):", rows_clues)
    else:
        print("Lỗi: AI không nhận diện được chữ số nào hợp lệ, hoặc thuật toán chia ô bị sai.")


if __name__ == "__main__":
    # Bây giờ bạn chỉ cần truyền đúng TÊN FILE ảnh, 
    # code sẽ tự động tìm nó trong thư mục 'res'.
    run_pipeline("test_image.jpg")