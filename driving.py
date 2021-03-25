import cv2
import numpy as np

def selectByDegree(mask, hough_value):
    #배열 차원 줄이기
    hough_value = np.squeeze(hough_value)

    for i,v in enumerate(hough_value):
        if v[1] < v[3]:
            hough_value[i] = np.array([v[2],v[3],v[0],v[1]])

    # 기울기 구하기
    slope_degree = (np.arctan2(hough_value[:, 1] - hough_value[:, 3], hough_value[:, 0] - hough_value[:, 2]) * 180) / np.pi

    # 기울기 평균 구하기
    avr_degree = sum(slope_degree)/len(slope_degree)

    # 평균 기울기와 비교해서 +-10도  미달 또는 초과하면 저장하지 않음
    hough_value_Result = hough_value[slope_degree > avr_degree-10]
    slope_degree_Result = slope_degree[slope_degree > avr_degree-10]
    hough_value_Result = hough_value[slope_degree_Result < avr_degree+10]
    slope_degree_Result = slope_degree_Result[slope_degree_Result < avr_degree+10]

    return hough_value_Result


def draw_road(argLine_img, argLine1, argLine2, argMiddleLine):
    # Right line
    cv2.line(argLine_img, (argLine2[0], argLine2[1]),
             (argLine2[2], argLine2[3]), (255, 0, 0), 20)

    # middle line
    cv2.line(argLine_img, (argMiddleLine[0], argMiddleLine[1]),
             (argMiddleLine[2], argMiddleLine[3]), (0, 255, 0), 20)

    # Left line
    cv2.line(argLine_img, (argLine1[0], argLine1[1]),
             (argLine1[2], argLine1[3]), (255, 0, 0), 20)

    return argLine_img

def getMiddleLine(argLine):
    i = 0
    permutation = np.argsort([2, 3, 0, 1])
    while i < len(argLine):
        if argLine[i][1] < argLine[i][3]:
            argLine[i] = argLine[i][permutation]

        i += 1

    line1 = np.empty((0, 4), int)
    line2 = np.empty((0, 4), int)

    try:
        standard = argLine[0][0]
        for v in argLine:
            if v[0] < standard+50:
                if v[0] > standard-50:
                    line1 = np.append(line1, np.array(
                        [[int(v[0]), int(v[1]), int(v[2]), int(v[3])]]), axis=0)

                else:
                    line2 = np.append(line2, np.array(
                        [[int(v[0]), int(v[1]), int(v[2]), int(v[3])]]), axis=0)

            else:
                line2 = np.append(line2, np.array(
                    [[int(v[0]), int(v[1]), int(v[2]), int(v[3])]]), axis=0)
        x1, y1 = int(sum(line1[:, 0])/len(line1)
                     ), int(sum(line1[:, 1])/len(line1))

        x2, y2 = int(sum(line1[:, 2])/len(line1)
                     ), int(sum(line1[:, 3])/len(line1))

        x3, y3 = int(sum(line2[:, 0])/len(line2)
                     ), int(sum(line2[:, 1])/len(line2))

        x4, y4 = int(sum(line2[:, 2])/len(line2)
                     ), int(sum(line2[:, 3])/len(line2))

        x5, y5 = int((x1 + x3)/2), int((y1 + y3)/2)
        x6, y6 = int((x2 + x4)/2), int((y2 + y4)/2)
        result_line1 = np.array([x1, y1, x2, y2])
        result_line2 = np.array([x3, y3, x4, y4])
        result_middle = np.array([x5, y5, x6, y6])
        argLine = np.array([argLine])

        return result_line1, result_line2, result_middle

    except:
        return False



def getMiddleDgreedAndCenter(lines_fit):
    result = (np.arctan2(lines_fit[2][1] - lines_fit[2][3], lines_fit[2][0] - lines_fit[2][2]) * 180) / np.pi
    result -= 90
    center = round((lines_fit[2][0]-320)/3.2)

    return result, center


def getLineImage(lines_fit1):
    # 결과에 따른 선 그리기
    black_img = np.zeros((480, 640, 3), dtype=np.uint8)
    lines_image = draw_road(black_img, lines_fit1[0], lines_fit1[1], lines_fit1[2])

    cv2.line(lines_image, (lines_fit1[2][0], lines_fit1[2][1]), (lines_fit1[2][0], lines_fit1[2][1]), (0, 0, 255), 20)

    return lines_image

def handling(slope_degree, center, op, handling):
    if -5 < slope_degree < 5:
        op='5'
        handling = "Middle"
    else:
        if slope_degree < 0:
            if -10 <= slope_degree:
                op='6'
                handling = "Right 1"
            elif -15 <= slope_degree:
                op='7'
                handling = "Right 2"
            elif -20 <= slope_degree:
                op='8'
                handling = "Right 3"
            else:
                op='9'
                handling = "Right 4"
        else:
            if  slope_degree < 10:
                op='4'
                handling = "Left 1"
            elif slope_degree < 15:
                op='3'
                handling = "Left 2"
            elif slope_degree < 20:
                op='2'
                handling = "Left 3"
            else:
                op='1'
                handling = "left 4"


    if op == '5':
        if  -3 < center < 3:
            op='5'
            handling = "Middle"
        else:
            if slope_degree < 0:
                if -5 <= center:
                    op='6'
                    handling = "Middle right 1"
                elif -10 <= center:
                    op='7'
                    handling = "Middle right 2"
                elif -15 <= center:
                    op='8'
                    handling = "Middle right 3"
                else:
                    op='9'
                    handling = "Middle right 4"
            else:
                if  center < 5:
                    op='4'
                    handling = "Middle left 1"
                elif center < 10:
                    op='3'
                    handling = "Middle left 2"
                elif center < 15:
                    op='2'
                    handling = "Middle left 3"
                else:
                    op='1'
                    handling = "Middle left 4"

    return op, handling


def putInfoText(argImage, degreeStr, centerStr, handlingStr, argColor):
    cv2.putText(argImage, degreeStr, (20, 400),cv2.FONT_HERSHEY_SIMPLEX, 1, argColor,2,cv2.LINE_AA)
    cv2.putText(argImage, centerStr, (20, 350),cv2.FONT_HERSHEY_SIMPLEX, 1, argColor,2,cv2.LINE_AA)
    cv2.putText(argImage, handlingStr, (400, 350),cv2.FONT_HERSHEY_SIMPLEX, 1, argColor,2,cv2.LINE_AA)

def driveCar(ser, argOp, argLastOrder):
    if argOp != argLastOrder:
        ser.write(op.encode())
        return argOp
    else:
        return argLastOrder
