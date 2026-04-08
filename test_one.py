import cv2
import sys
import os
from pathlib import Path

# Thêm thư mục code vào Python path
sys.path.insert(0, str(Path("d:/Chuyen giao/project/nonogram/nonogram_solver/code").resolve()))

from util.nonogram import Nonogram
from nonogram_detector.binarize_fn import binarize_adaptive_threshold, binarize_fixed_threshold
from nonogram_detector.nonogram_detector import NonogramDetector
from nonogram_detector.rectangle_fn import rectangle_approx_poly
from perspective_transformer.perspective_transformer import PerspectiveTransformer
from line_detector.line_detector import LinesDetector
from line_detector.line_detector_fn import lines_nxm_kernel
from digit_detector.digit_detector import DigitDetector
from digit_classifier.mask_classifier import MaskClassifier
from nonogram_solver.nonogram_solver import NonogramSolver

def test():
    image_path = Path("d:/Chuyen giao/project/nonogram/nonogram_solver/res/test/i8750/imgs_05x05/img_02.jpg")
    masks_path = "d:/Chuyen giao/project/nonogram/nonogram_solver/res/digits_00/masks"

    nonogram_detector = NonogramDetector(binarize_adaptive_threshold, rectangle_approx_poly)
    transformer = PerspectiveTransformer(binarize_fixed_threshold(200), binarize_adaptive_threshold)
    line_detector = LinesDetector(lines_nxm_kernel)
    classifier = MaskClassifier(masks_path=str(masks_path))
    digit_detector = DigitDetector(classifier)
    nonogram_solver = NonogramSolver()

    img = cv2.imread(str(image_path))
    
    # Run steps manually to see where it breaks
    resized_img, img_bin, rects = nonogram_detector.detect(img)
    print("Detected rects:", len(rects) if rects else 0)
    
    if rects:
        rects = sorted(rects, key=cv2.contourArea, reverse=True)
        rect = rects[0]
        
        cv2.imwrite("debug_1_resized.jpg", resized_img)
        cv2.imwrite("debug_2_img_bin.jpg", img_bin)
        
        transformer.set_image(resized_img)
        transformer.set_contour(rect)
        img_wrapped = transformer.get_result()
        
        cv2.imwrite("debug_3_wrapped.jpg", img_wrapped)

        line_detector.set_image(img_wrapped)
        imgs, coords = line_detector.get_result()
        
        cv2.imwrite("debug_4_lines_v.jpg", imgs[0])
        cv2.imwrite("debug_5_lines_h.jpg", imgs[1])
        
        print(f"Num horiz lines: {len(coords[1])}, Num vertical lines: {len(coords[0])}")
        
        # Merge
        img_merge = cv2.add(img_wrapped, cv2.add(imgs[0], imgs[1]))
        cv2.imwrite("debug_6_merge.jpg", img_merge)

        digit_detector.set_image(img_merge)
        digit_detector.set_lines(*coords)
        
        final_img, nonogram_values = digit_detector.get_result()
        if nonogram_values:
            cols, rows = nonogram_values
            print(f"Cols: {len(cols)}, Rows: {len(rows)}")
        else:
            print("Digit detector returned None")
            lv, lh = coords
            print(f"Passed lv: {lv}")
            print(f"Passed lh: {lh}")

test()
