import time

import cv2
import numpy as np

cap = cv2.VideoCapture(1)

n = int(input("Số lượng bức ảnh chụp: "))
distance = int(input("Khoảng cách giữa mỗi lần chụp: "))

# for i in range(n):
#     ret, frame = cap.read()
#     cv2.imwrite(f"Ima/image_{i}.jpg", frame)
#     cv2.waitKey(distance * 60 * 1000)


def Save_Auto_Camera(counters, timers):
    for i in range(counters):
        ret, frame = cap.read()
        localtime = time.localtime(time.time())
        read_time = str(localtime.tm_hour) + 'h' + str(localtime.tm_min) + 'm' + str(i + 1)
        path_Camera = 'Ima/Image_' + read_time + '.jpg'
        cv2.imwrite(path_Camera, frame)
        cv2.waitKey(timers * 60 * 1000)
    print("Đã đủ ảnh. Thực hiện việc khác")


Save_Auto_Camera(n, distance)
cap.release()
cv2.destroyAllWindows()
