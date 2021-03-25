import cv2
import numpy as np

def draw_lines(img, lines, color=[255, 0, 0], thickness=5):
    for line in lines:
        for x1, y1, x2, y2 in line:
            cv2.line(img, (x1, y1), (x2, y2), color, thickness)


def hough_lines_value(img):
    # hough_line 파라미터
    rho = 1
    theta = np.pi/180
    threshold = 50
    min_line_len = 10
    max_line_gap = 50

    lines = cv2.HoughLinesP(img, rho, theta, threshold, np.array([]), minLineLength=min_line_len, maxLineGap=max_line_gap)

    return lines


def hough_lines_image(img):
    # hough_line 파라미터
    rho = 1
    theta = np.pi/180
    threshold = 50
    min_line_len = 10
    max_line_gap = 50

    lines = cv2.HoughLinesP(img, rho, theta, threshold, np.array([]), minLineLength=min_line_len, maxLineGap=max_line_gap)

    # 선 그리기
    line_img = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
    draw_lines(line_img, lines)

    return line_img
