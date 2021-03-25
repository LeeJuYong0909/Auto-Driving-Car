import cv2
import numpy as np
import matplotlib.pyplot as plt
import serial

import correction as correct
import recognition as recognize
import driving as drive

vertices1 = np.array([[(290, 430), (180, 250), (480, 250), (350, 430)]], dtype=np.int32)
vertices2 = np.array([[(160, 250), (160, 50), (480, 50), (480, 250)]], dtype=np.int32)


# ------------------------------------영상 설정--------------------------------------
cap = cv2.VideoCapture(-1)
fileName = 'recording.avi'
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)

# 재생할 파일의 높이 얻기
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

# 재생할 파일의 프레임 레이트 얻기
fps = cap.get(cv2.CAP_PROP_FPS)

out = cv2.VideoWriter(fileName, cv2.VideoWriter_fourcc(*'XVID'), fps, (int(width), int(height)))
# -------------------------------------------------------------------------------
lines_fit1 = []
# lines_fit2 = []

slope_degree = 0            # default
center = 0                  # default

op = 's'                    # 모터 명령어
lastorder   = 's'           # 중복 명령 방지용
handling    = "None"        # 모터 명령어 확인용
centerStr   = "Center: "    # 중앙 위치 확인용
degreeStr   = 'Degree: '    # 각도 확인용

# Arduino (motor)
ser = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate=9600,
)

while(cap.isOpened()):

    ret, frame = cap.read()

    # 새눈 함수
    birdView = correct.bird_eye_view(frame)

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
        lines_fit1 = drive.selectByDegree(mask1, hough_value)

        # 위치에따른 차선 구분
        lines_fit1 = drive.getMiddleLine(lines_fit1)

        #각도와 중앙 위치 측정
        slope_degree, center = drive.getMiddleDgreedAndCenter(lines_fit1)
        centerStr   += str(round(center))
        degreeStr   += str(round(slope_degree))

        # 핸들링
        op, handling = drive.handling(slope_degree, center, op, handling)

        # 아두이노 모터제어
        lastOrder = drive.driveCar(ser, op, lastOrder)

        # 인식한 차선과 이미지 합치기
        lines_image = drive.getLineImage(lines_fit1)
        combo_image = cv2.addWeighted(birdView, 0.8, lines_image, 1, 1)

        # 결과값 화면에 출력
        drive.putInfoText(combo_image, degreeStr, centerStr, handling)

        # 결과 화면 출력
        cv2.imshow('result', combo_image)

        # 결과 화면 녹화
        out.write(combo_image)

    except: # 에러방생
        # 정지
        lastOrderdrive.driveCar(ser, 's', lastOrder)

        # 화면 글씨 빨간색으로 변경
        drive.putInfoText(birdView, degreeStr, centerStr, handling)

        # 기본 이미지 출력
        cv2.imshow('result', birdView)

        # 기본 화면 녹화
        out.write(birdView)

    k = cv2.waitKey(1) & 0xFF
    if(k == 27):
        break

cap.release()
out.release()
cv2.destroyAllWindows()
