import cv2
import numpy as np
from operator import itemgetter

class DigitDetector:
    def __init__(self, classifier):
        self.classifier = classifier
        self.image = None
        self.lines = None

    def set_image(self, image):
        self.image = image

    def set_lines(self, lines_v, lines_h):
        self.lines = (lines_v, lines_h)

    @staticmethod
    def _extract_number(digits):
        """Helper: Chuyển danh sách chữ số thành số nguyên duy nhất."""
        num = 0
        for d in digits:
            num = num * 10 + d
        return num

    def _process_cell(self, region, x_offset, y_offset, display_img):
        """Xử lý một ô cụ thể để nhận diện các chữ số bên trong."""
        h_reg, w_reg = region.shape
        min_h, min_w = h_reg / 3.0, h_reg / 6.0
        
        # Tìm contours trong ô
        contours, _ = cv2.findContours(region, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        found_digits = []
        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            # Lọc theo kích thước thực tế của chữ số trong Nonogram
            if 3 * min_h > h > min_h and 4 * min_w > w > min_w:
                digit_roi = 255 - region[y:y+h, x:x+w]
                # Nhận diện
                preds = self.classifier.classify(digit_roi)
                val = sorted(preds)[0][1] # Lấy nhãn có khoảng cách/xác suất tốt nhất
                
                # Vẽ debug trực tiếp lên ảnh kết quả
                cv2.rectangle(display_img, (x+x_offset, y+y_offset), 
                             (x+w+x_offset, y+h+y_offset), (0, 255, 0), 1)
                found_digits.append((x, y, w, h, val))
        
        return found_digits

    def get_result(self):
        if self.image is None or self.lines is None:
            return None, None

        lv, lh = self.lines
        # Tiền xử lý ảnh nhị phân để tìm contour nhanh hơn
        _, binary_img = cv2.threshold(self.image, 127, 255, cv2.THRESH_BINARY_INV)
        display_img = cv2.cvtColor(self.image, cv2.COLOR_GRAY2BGR)
        
        cols_clues = [] # Gợi ý cho các cột (nằm ở hàng 0)
        rows_clues = [] # Gợi ý cho các hàng (nằm ở cột 0)

        # 1. Quét hàng tiêu đề (Gợi ý cho các Cột)
        for i in range(1, len(lv) - 1):
            x1, x2, y1, y2 = int(lv[i]+1), int(lv[i+1]-1), int(lh[0]+1), int(lh[1]-1)
            cell_roi = binary_img[y1:y2, x1:x2]
            digits = self._process_cell(cell_roi, x1, y1, display_img)
            if digits:
                # Sắp xếp theo y (dọc) rồi ghép số
                nums = self._get_numbers_from_digits(digits, mode='vertical')
                cols_clues.append(nums)

        # 2. Quét cột tiêu đề (Gợi ý cho các Hàng)
        for j in range(1, len(lh) - 1):
            x1, x2, y1, y2 = int(lv[0]+1), int(lv[1]-1), int(lh[j]+1), int(lh[j+1]-1)
            cell_roi = binary_img[y1:y2, x1:x2]
            digits = self._process_cell(cell_roi, x1, y1, display_img)
            if digits:
                # Sắp xếp theo x (ngang) rồi ghép số
                nums = self._get_numbers_from_digits(digits, mode='horizontal')
                rows_clues.append(nums)

        # Kiểm tra logic Nonogram: Tổng các số hàng = Tổng các số cột
        sum_cols = sum(sum(c) for c in cols_clues)
        sum_rows = sum(sum(r) for r in rows_clues)

        if sum_cols == sum_rows and sum_cols > 0:
            return display_img, (cols_clues, rows_clues)
        return display_img, None

    def _get_numbers_from_digits(self, digits, mode='horizontal'):
        """
        Logic ghép các contour chữ số rời rạc thành danh sách các số.
        Ví dụ: Trong 1 ô có contour '1' và '5' -> Ghép thành số 15.
        """
        if not digits: return []
        
        # Sắp xếp theo chiều đọc (Ngang: x tăng dần, Dọc: y tăng dần)
        primary_idx = 0 if mode == 'horizontal' else 1
        sorted_digits = sorted(digits, key=itemgetter(primary_idx))
        
        numbers = []
        current_group = [sorted_digits[0][4]]
        
        # Ngưỡng khoảng cách để coi là cùng một số (epsilon)
        eps = 5 
        
        for k in range(1, len(sorted_digits)):
            prev = sorted_digits[k-1]
            curr = sorted_digits[k]
            
            # Nếu khoảng cách quá xa, coi là số mới (trong Nonogram thường là 1 ô 1 số)
            # Nhưng đôi khi 1 ô có nhiều số xếp chồng
            dist = curr[primary_idx] - (prev[primary_idx] + prev[primary_idx+2])
            if dist > eps:
                numbers.append(self._extract_number(current_group))
                current_group = [curr[4]]
            else:
                current_group.append(curr[4])
        
        numbers.append(self._extract_number(current_group))
        return numbers