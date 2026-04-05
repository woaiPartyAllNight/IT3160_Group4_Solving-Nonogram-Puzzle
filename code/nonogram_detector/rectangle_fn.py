import cv2
from util.config import Config

def rectangle_approx_poly(contour):
    epsilon = Config.epsilon * cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, epsilon, True)
    
    # Kiểm tra có đúng 4 đỉnh VÀ phải là một đa giác lồi
    if len(approx) == 4 and cv2.isContourConvex(approx):
        return approx
        
    return None