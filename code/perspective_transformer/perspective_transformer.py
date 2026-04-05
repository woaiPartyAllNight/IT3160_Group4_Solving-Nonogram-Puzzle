import cv2
import numpy as np
from typing import Callable, Optional

# Giả sử bạn đã có module này trong project
from util.benchmark import timeit

class PerspectiveTransformer:
    def __init__(self, 
                fixed_binarize_fn: Optional[Callable] = None, 
                adaptive_binarize_fn: Optional[Callable] = None):
        """
        Khởi tạo Transformer với các hàm binarize (nhị phân hóa) tùy chọn.
        """
        self.fixed_binarize_fn = fixed_binarize_fn
        self.adaptive_binarize_fn = adaptive_binarize_fn
        self.image: Optional[np.ndarray] = None
        self.contour: Optional[np.ndarray] = None

    def set_image(self, image: np.ndarray) -> None:
        """Thiết lập ảnh đầu vào. Tự động áp dụng adaptive binarize nếu có."""
        if self.adaptive_binarize_fn is not None:
            gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
            self.image = self.adaptive_binarize_fn(gray)
        else:
            # Dùng copy() để tránh vô tình thay đổi ảnh gốc bên ngoài class
            self.image = image.copy()

    def set_contour(self, contour: np.ndarray) -> None:
        """Thiết lập đường viền (contour) của tài liệu/đối tượng cần cắt."""
        self.contour = contour

    def create_rect(self) -> np.ndarray:
        """Xác định 4 góc của hình chữ nhật từ contour."""
        if self.contour is None:
            raise ValueError("Contour chưa được thiết lập. Hãy gọi set_contour() trước.")

        # [TỐI ƯU HÓA]: Bỏ vòng lặp for chậm chạp, dùng reshape của numpy (Vector hóa)
        points = self.contour.reshape(-1, 2).astype(np.float32)
        rect = np.zeros((4, 2), dtype=np.float32)

        # Tính tổng và hiệu của các tọa độ (x, y)
        s = points.sum(axis=1)
        diff = np.diff(points, axis=1)

        # Top-Left (tổng nhỏ nhất), Bottom-Right (tổng lớn nhất)
        rect[0] = points[np.argmin(s)]
        rect[2] = points[np.argmax(s)]

        # Top-Right (hiệu nhỏ nhất), Bottom-Left (hiệu lớn nhất)
        rect[1] = points[np.argmin(diff)]
        rect[3] = points[np.argmax(diff)]

        return rect

    @timeit
    def get_result(self) -> np.ndarray:
        """Thực hiện biến đổi phối cảnh (perspective transform) để cắt phẳng ảnh."""
        if self.image is None or self.contour is None:
            raise ValueError("Image hoặc Contour chưa được thiết lập. Không thể xử lý.")

        rect = self.create_rect()
        (tl, tr, br, bl) = rect

        # [TỐI ƯU HÓA]: Sử dụng np.linalg.norm để tính khoảng cách Euclid (chuẩn L2) nhanh và gọn hơn
        width_a = np.linalg.norm(br - bl)
        width_b = np.linalg.norm(tr - tl)
        max_width = max(int(width_a), int(width_b))

        height_a = np.linalg.norm(tr - br)
        height_b = np.linalg.norm(tl - bl)
        max_height = max(int(height_a), int(height_b))

        # Khai báo tọa độ đích của ảnh mới (chữ nhật vuông vức)
        dst = np.array([
            [0, 0],
            [max_width - 1, 0],
            [max_width - 1, max_height - 1],
            [0, max_height - 1]
        ], dtype=np.float32)

        # Tính toán ma trận biến đổi phối cảnh và áp dụng lên ảnh
        matrix = cv2.getPerspectiveTransform(rect, dst)
        warped = cv2.warpPerspective(self.image, matrix, (max_width, max_height))

        # Áp dụng bộ lọc nhị phân tĩnh (nếu có)
        if self.fixed_binarize_fn is not None:
            warped = self.fixed_binarize_fn(warped)

        return warped