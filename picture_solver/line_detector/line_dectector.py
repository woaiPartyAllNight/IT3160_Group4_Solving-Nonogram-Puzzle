import numpy as np
from util.benchmark import timeit

class LinesDetector:
    def __init__(self, line_detection_fn):
        self.image = None
        self.line_detection_fn = line_detection_fn

    def set_image(self, image):
        self.image = image

    @staticmethod
    def get_lines_coordinates(sum_array, length):
        """
        Tìm tọa độ trung tâm của các đường kẻ dựa trên mảng tổng (lược đồ chiếu).
        """
        # Ngưỡng: Ít nhất 33% độ dài đường kẻ phải là pixel sáng
        threshold = (255 * length) / 3
        
        # Lấy ra TẤT CẢ các chỉ số (index) vượt ngưỡng bằng NumPy (Nhanh hơn vòng lặp for)
        valid_indices = np.where(sum_array > threshold)[0]

        # Xử lý an toàn nếu không tìm thấy đường kẻ nào
        if len(valid_indices) == 0:
            return []

        # Tính khoảng cách giữa các pixel liền kề
        diffs = np.diff(valid_indices)
        
        # Nếu chỉ có đúng 1 pixel vượt ngưỡng, trả về luôn tọa độ đó
        if len(diffs) == 0:
            return [float(valid_indices[0])]

        # Khoảng cách tối đa để gom nhóm (gom các pixel thuộc cùng 1 nét vẽ dày)
        eps = 2 * np.mean(diffs)
        eps = max(eps, 2.0) # Đảm bảo eps tối thiểu là 2 để không bị lỗi chia cắt nét

        result_coordinates = []
        current_group_indices = [valid_indices[0]]
        current_group_weights = [sum_array[valid_indices[0]]]

        # Duyệt để gom nhóm và tính trọng tâm
        for i in range(1, len(valid_indices)):
            idx = valid_indices[i]
            
            if idx - current_group_indices[-1] < eps:
                # Pixel nằm sát nhau -> Cùng một nét vẽ
                current_group_indices.append(idx)
                current_group_weights.append(sum_array[idx])
            else:
                # Cách xa nhau -> Đã sang nét vẽ mới. Tính trọng tâm của nét cũ.
                # Công thức tính trung bình có trọng số (Center of Mass)
                center = np.average(current_group_indices, weights=current_group_weights)
                result_coordinates.append(center)
                
                # Reset để gom nhóm mới
                current_group_indices = [idx]
                current_group_weights = [sum_array[idx]]

        # Tính toán cho nhóm nét vẽ cuối cùng (thay cho thủ thuật 16*Config cũ)
        if current_group_indices:
            center = np.average(current_group_indices, weights=current_group_weights)
            result_coordinates.append(center)

        return result_coordinates

    @timeit
    def get_result(self):
        if self.image is None:
            raise ValueError("Chưa cung cấp ảnh đầu vào. Vui lòng gọi set_image() trước.")
            
        img_v, img_h = self.line_detection_fn(self.image)
        coords_v = self.get_lines_coordinates(img_v.sum(axis=0), self.image.shape[0])
        coords_h = self.get_lines_coordinates(img_h.sum(axis=1), self.image.shape[1])
        return (img_v, img_h), (coords_v, coords_h)