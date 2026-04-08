import cv2
from pathlib import Path
from util.benchmark import timeit

class Nonogram:
    @timeit
    def __init__(self, image, nonogram_detector, perspective_transformer, line_detector,
                digit_detector, digit_classifier, nonogram_solver, solution_creator=None):
        self.nonogram_detector = nonogram_detector
        self.perspective_transformer = perspective_transformer
        self.line_detector = line_detector
        self.digit_detector = digit_detector
        self.digit_classifier = digit_classifier
        self.nonogram_solver = nonogram_solver
        self.solution_creator = solution_creator
        
        # [CẢI TIẾN 1]: Thay `basestring` (chỉ có ở Python 2) bằng `(str, Path)`
        # Điều này giúp hàm nhận được cả đường dẫn dạng chuỗi cũ và đối tượng Path mới.
        if isinstance(image, (str, Path)):
            self.image = cv2.imread(str(image))
        else:
            self.image = image

    @timeit
    def solve(self):
        result = []
        resized_img, img_bin, rects = self.nonogram_detector.detect(self.image)

        # [CẢI TIẾN 2]: Lọc nhiễu
        # Sắp xếp các khung chữ nhật tìm được theo diện tích từ lớn đến bé.
        # Đảm bảo khung bảng Nonogram thật (thường là to nhất) sẽ được xử lý đầu tiên.
        if rects:
            rects = sorted(rects, key=cv2.contourArea, reverse=True)

        for rect in rects:
            self.perspective_transformer.set_image(resized_img)
            self.perspective_transformer.set_contour(rect)
            img_wrapped = self.perspective_transformer.get_result()

            self.line_detector.set_image(img_wrapped)
            imgs, coords = self.line_detector.get_result()
            
            # Bỏ `cv2.add` vì `img_wrapped` là nền trắng nét đen, còn `imgs` là nền đen nét trắng. Gộp lại sẽ ra trắng tinh 100%.
            self.digit_detector.set_image(img_wrapped)
            self.digit_detector.set_lines(*coords)
            img, nonogram_values = self.digit_detector.get_result()

            if nonogram_values is None:
                result.append(img)
                # [CẢI TIẾN 3]: Đổi cú pháp print của Python 2 sang hàm print() của Python 3
                print("⚠️ Cảnh báo: Không thể nhận diện hoặc giải Nonogram ở khung này!")
                continue

            self.nonogram_solver.set_values(*nonogram_values)
            self.nonogram_solver.solve()
            solution = self.nonogram_solver.get_solution()

            if self.solution_creator is not None:
                self.solution_creator.set_image(img_wrapped)
                self.solution_creator.set_coordinates(coords)
                self.solution_creator.set_solution(solution)
                img = self.solution_creator.get_result()

            result.append(img)
            
            # [CẢI TIẾN 4]: Giả định mỗi ảnh chụp chỉ có 1 bảng Nonogram.
            # Nếu đã giải thành công bảng lớn nhất, thoát vòng lặp để tránh AI đi giải nhầm 
            # các vết xước/ô vuông nhiễu nhỏ xíu ở hậu cảnh.
            break 

        return result