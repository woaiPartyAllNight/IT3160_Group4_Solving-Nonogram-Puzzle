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

def lines_nxm_kernel(image, n=40, m=1):
    """
    Phát hiện các đường kẻ dọc và ngang từ ảnh.
    Đầu vào có thể là chữ đen nền trắng hoặc chữ trắng nền đen.
    """
    import numpy as np
    # Đảo màu nếu nền đang là trắng (để về đúng chuẩn nền đen nét trắng cho MORPH_OPEN)
    if np.mean(image) > 127:
        process_img = cv2.bitwise_not(image)
    else:
        process_img = image

    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (n, m))
    horizontal_lines = cv2.morphologyEx(process_img, cv2.MORPH_OPEN, horizontal_kernel)
    
    vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (m, n))
    vertical_lines = cv2.morphologyEx(process_img, cv2.MORPH_OPEN, vertical_kernel)
    
    return vertical_lines, horizontal_lines