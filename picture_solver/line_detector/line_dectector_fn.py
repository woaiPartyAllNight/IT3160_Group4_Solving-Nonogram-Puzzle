import cv2
import numpy as np

def extract_lines_easy(image_path):
    # 1. Đọc ảnh và chuyển sang chế độ xám (Grayscale)
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # 2. Nhị phân hóa (Binarization) và đảo ngược màu (Nền đen, nét trắng)
    _, thresh = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)

    # 3. Định nghĩa các Kernel (Cái khuôn)
    # Khuôn nằm ngang (Rộng 40 pixel, cao 1 pixel)
    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40, 1))
    # Khuôn thẳng đứng (Rộng 1 pixel, cao 40 pixel)
    vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 40))

    # 4. Áp dụng Phép Mở (Morphological Open) để lọc nét
    horizontal_lines = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, horizontal_kernel)
    vertical_lines = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, vertical_kernel)

    # 5. Gộp nét ngang và dọc lại thành một lưới hoàn chỉnh (ví dụ: khung bảng)
    grid = cv2.add(horizontal_lines, vertical_lines)

    return grid