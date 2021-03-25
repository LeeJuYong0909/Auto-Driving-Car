import cv2
import numpy as np

def bird_eye_view(img):

    IMAGE_H = 480

    IMAGE_W = 640

    src = np.float32([[0, IMAGE_H], [640, IMAGE_H], [0, 0], [IMAGE_W, 0]])

    dst = np.float32([[300, IMAGE_H], [340, IMAGE_H], [0, 0], [IMAGE_W, 0]])

    M = cv2.getPerspectiveTransform(src, dst)  # The transformation matrix

    Minv = cv2.getPerspectiveTransform(dst, src)  # Inverse transformation

    img = img[260:(260+IMAGE_H), 0:IMAGE_W]  # Apply np slicing for ROI crop

    warped_img = cv2.warpPerspective(
        img, M, (IMAGE_W, IMAGE_H))  # Image warping

    return warped_img

def grayscale(img):
    return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)


def gaussian_blur(img):
    kernel_size = 9

    return cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)


def canny(img):
    lowThreshold = 50
    highThreshold = 100

    return cv2.Canny(img, lowThreshold, highThreshold)


def region_of_interest(img, vertices):
    mask = np.zeros_like(img)
    if len(img.shape) > 2:
        channel_count = img.shape[2]
        ignore_mask_color = (255,) * channel_count

    else:
        ignore_mask_color = 255

    cv2.fillPoly(mask, vertices, ignore_mask_color)
    masked_image = cv2.bitwise_and(img, mask)
    return masked_image
