import cv2
import numpy as np
from typing import Callable

def binarize_adaptive_threshold(
    img: np.ndarray, 
    block_size: int = 11, 
    c: float = 2.0, 
    max_val: int = 255
) -> np.ndarray:
    """
    Nhị phân hóa ảnh sử dụng ngưỡng thích ứng Gaussian.
    
    Args:
        img: Ảnh đầu vào (numpy array).
        block_size: Kích thước vùng lân cận để tính ngưỡng (phải là số lẻ).
        c: Hằng số trừ đi từ giá trị trung bình tính toán được.
        max_val: Giá trị gán cho các pixel vượt ngưỡng (thường là 255).
        
    Returns:
        np.ndarray: Ảnh nhị phân đã xử lý.
    """
    # Đảm bảo ảnh đầu vào là ảnh xám (Grayscale) vì adaptiveThreshold chỉ nhận ảnh 1 kênh màu
    if len(img.shape) > 2 and img.shape[2] == 3:
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        img_gray = img

    return cv2.adaptiveThreshold(
        img_gray, 
        max_val, 
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
        cv2.THRESH_BINARY_INV, 
        block_size, 
        c
    )


def binarize_fixed_threshold(
    threshold: int = 128, 
    max_val: int = 255
) -> Callable[[np.ndarray], np.ndarray]:
    """
    Tạo hàm nhị phân hóa ảnh sử dụng ngưỡng cố định toàn cục.
    
    Args:
        threshold: Giá trị ngưỡng cố định (0-255).
        max_val: Giá trị gán cho các pixel vượt ngưỡng.
        
    Returns:
        Một hàm nhận đầu vào là ảnh và trả về ảnh nhị phân.
    """
    def func(img: np.ndarray) -> np.ndarray:
        # Tương tự, đảm bảo ảnh là ảnh xám trước khi xử lý
        if len(img.shape) > 2 and img.shape[2] == 3:
            img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        else:
            img_gray = img
            
        _, ret = cv2.threshold(img_gray, threshold, max_val, cv2.THRESH_BINARY_INV)
        return ret

    return func