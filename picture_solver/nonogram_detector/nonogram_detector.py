import cv2
from util.config import Config
from util.benchmark import timeit

class NonogramDetector:
    def __init__(self, binarize_fn, rectangle_fn):
        """Khởi tạo detector với các hàm xử lý tùy chỉnh (Dependency Injection)."""
        self.binarize_fn = binarize_fn
        self.rectangle_fn = rectangle_fn

    @timeit
    def resize_image(self, image):
        """Thu phóng ảnh về kích thước chuẩn."""
        if image is None:
            raise ValueError("Ảnh đầu vào không được để trống (None).")
        factor = Config.image_width / image.shape[1]
        return cv2.resize(image, (0, 0), fx=factor, fy=factor, interpolation=Config.interpolation)

    @timeit
    def to_grayscale(self, image):
        """Đổi hệ màu ảnh sang xám (Grayscale)."""
        return cv2.cvtColor(image, Config.cvt_color_code)

    @staticmethod
    def check_minimal_size(contour):
        """Kiểm tra contour có đạt chuẩn về kích thước và tỷ lệ hay không."""
        x, y, w, h = cv2.boundingRect(contour)
        # Trả về kết quả đánh giá biểu thức logic thay vì dùng câu lệnh if
        return (h > Config.d_min and 
                w > Config.d_min and 
                (1.0 / Config.aspect_ratio) < (1.0 * h / w) < Config.aspect_ratio)

    @timeit
    def find_rectangles(self, binary_image):
        """Tìm các hình chữ nhật từ ảnh nhị phân."""
        rects = []
        # Tương thích với OpenCV 4.x (chỉ nhận 2 giá trị trả về)
        contours, hierarchy = cv2.findContours(binary_image, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        
        for contour in contours:
            if self.check_minimal_size(contour):
                rect = self.rectangle_fn(contour)
                if rect is not None:
                    rects.append(contour)

        return rects

    @timeit
    def detect(self, original_image):
        """
        Luồng thực thi chính: Xử lý từ ảnh gốc thành danh sách các khung Nonogram.
        Thay thế cho hàm get_result() cũ.
        """
        # Bước 1: Thu phóng ảnh
        resized_img = self.resize_image(original_image)
        
        # Bước 2: Đổi màu ảnh (xám hóa)
        gray_img = self.to_grayscale(resized_img)
        
        # Bước 3: Nhị phân hóa
        binary_img = self.binarize_fn(gray_img)
        
        # Bước 4: Tìm đường viền chữ nhật
        rects = self.find_rectangles(binary_img)

        # Trả về ảnh đã thu phóng, ảnh nhị phân, và danh sách các khung lưới
        return resized_img, binary_img, rects