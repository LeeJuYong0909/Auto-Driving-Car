import cv2
import numpy as np
import matplotlib.pyplot as plt
import serial

import correction as correct
import recognition as recognize
import driving as drive

vertices1 = np.array([[(290, 430), (180, 250), (480, 250), (350, 430)]], dtype=np.int32)

lines_fit = []

slope_degree = 0            # default
center = 0                  # default

op = 's'                    # 모터 명령어
lastorder   = 's'           # 중복 명령 방지용
handling    = "None"        # 모터 명령어 확인용
centerStr   = "Center: "    # 중앙 위치 확인용
degreeStr   = 'Degree: '    # 각도 확인용
red         = (0,0,255)
yellow      = (0,255,0)

image = cv2.imread('TestTrack1.png')

# 새눈 함수
birdView = correct.bird_eye_view(image)

# 흑백처리 함수
gray = correct.grayscale(birdView)

# 흐림처리 함수
blurGray = correct.gaussian_blur(gray)

# 가장자리 추출 함수
edges = correct.canny(blurGray)

# 필요한 부분만보기
mask1 = correct.region_of_interest(edges, vertices1)
#mask2 = region_of_interest(edges, vertices2)

# 선 추출
hough_value = recognize.hough_lines_value(mask1)
hough_image = recognize.hough_lines_image(mask1)


try:
    # 각도 평균값 범위에 벗어나는 선 삭제
    lines_fit = drive.selectByDegree(mask1, hough_value)

    # 위치에따른 차선 구분
    lines_fit = drive.getMiddleLine(lines_fit)

    #각도와 중앙 위치 측정
    slope_degree, center = drive.getMiddleDgreedAndCenter(lines_fit)
    centerStr   += str(round(center))
    degreeStr   += str(round(slope_degree))

    # 핸들링
    op, handling = drive.handling(slope_degree, center, op, handling)

    # 인식한 차선과 이미지 합치기
    lines_image = drive.getLineImage(lines_fit)
    combo_image = cv2.addWeighted(birdView, 0.8, lines_image, 1, 1)

    # 결과값 화면에 출력
    drive.putInfoText(combo_image, degreeStr, centerStr, handling, yellow)
    cv2.imshow('result', combo_image)

except Exception as ex:
    print(ex)

    drive.putInfoText(birdView, degreeStr, centerStr, handling, red)
    cv2.imshow('result', hough_image)


k = cv2.waitKey(0)
if k == 27:# ESC키
    cv2.destroyAllWindows();
elif k == ord('s'): #저장하기 버튼
    cv2.imwrite("resultImage.png",combo_image)
    cv2.destroyAllWindows();
