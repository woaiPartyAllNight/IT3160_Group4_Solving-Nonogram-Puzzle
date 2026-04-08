import cv2
import numpy as np
import time
from pathlib import Path
from util.benchmark import timeit

# Giả lập Config nếu bạn chưa có file config.py
class Config:
    digit_size = (28, 28) # Kích thước chuẩn, ví dụ 28x28 pixel

class MaskClassifier:
    @timeit
    # digits_path: Thư mục chứa ảnh gốc của các chữ số (cấu trúc: digits/0, digits/1, ..., digits/9)
    # masks_path: Thư mục chứa các mask đã tạo sẵn (cấu trúc: masks/0.png, masks/1.png, ..., masks/9.png)
    def __init__(self, digits_path=None, masks_path=None):
        self.masks = [None] * 10

        if digits_path is not None:
            self.path = Path(digits_path)
            self.masks_path = self.path / 'masks'
            self.masks_path.mkdir(parents=True, exist_ok=True) # Tự động tạo thư mục nếu chưa có
            self.create_masks()
        elif masks_path is not None:
            self.masks_path = Path(masks_path)
            self.load_masks()

    @staticmethod
    def __create_mask(paths):
        mask = np.zeros(Config.digit_size, dtype='float32')
        for path in paths:
            img = cv2.imread(str(path), cv2.IMREAD_GRAYSCALE)
            if img is not None:
                img = cv2.resize(img, Config.digit_size)
                mask += img
        
        # Chuẩn hóa về thang 0-255 an toàn hơn
        if mask.max() > 0:
            mask = (mask / mask.max()) * 255.0
            
        return mask.astype('uint8')

    def create_masks(self):
        for i in range(10):
            # Tìm tất cả ảnh trong thư mục con tương ứng với số i
            digit_dir = self.path / str(i)
            if digit_dir.exists():
                paths = list(digit_dir.rglob('*.[pP][nN][gG]')) + list(digit_dir.rglob('*.[jJ][pP][gG]'))
                if paths:
                    mask = self.__create_mask(paths)
                    cv2.imwrite(str(self.masks_path / f'{i}.png'), mask)
                    self.masks[i] = mask.astype('int32')

    def load_masks(self):
        for i in range(10):
            mask_file = self.masks_path / f'{i}.png'
            if mask_file.exists():
                img = cv2.imread(str(mask_file), cv2.IMREAD_GRAYSCALE)
                mask = cv2.resize(img, Config.digit_size)
                self.masks[i] = mask.astype('int32')

    def classify(self, img):
        img = cv2.resize(img, Config.digit_size).astype('int32')
        results = []
        for i, mask in enumerate(self.masks):
            if mask is not None:
                # Tránh lỗi chia cho 0 nếu mask đen thui
                mask_sum = mask.sum()
                if mask_sum == 0: mask_sum = 1 
                
                score = 1.0 * np.abs(mask - img).sum() / mask_sum
                results.append((score, i))
        
        # Sắp xếp từ điểm khác biệt thấp nhất (giống nhất) đến cao nhất
        return sorted(results, key=lambda x: x[0])

    def test(self, root_path, full_log=False):
        root = Path(root_path)
        for i in range(10):
            print(f'---------- {i} ----------')
            count, error = 0, 0
            digit_dir = root / str(i)
            
            if not digit_dir.exists(): continue
            
            paths = list(digit_dir.rglob('*.*'))
            for path in paths:
                if path.is_file():
                    img = cv2.imread(str(path), cv2.IMREAD_GRAYSCALE)
                    if img is None: continue
                    
                    count += 1
                    digits = self.classify(img)

                    if full_log and len(digits) >= 2:
                        print(f"Top 1: Số {digits[0][1]} (Sai số: {digits[0][0]:.4f}) | Top 2: Số {digits[1][1]} (Sai số: {digits[1][0]:.4f})")

                    if i != digits[0][1]:
                        error += 1
                        print(f"Lỗi ở file {path.name}: {digits[:3]}") # Chỉ in top 3 để đỡ rối
                        
            if count > 0:
                print(f"Thành công: {100.0 * (count - error) / count:.2f}% - Tổng: {count}, Lỗi: {error}")