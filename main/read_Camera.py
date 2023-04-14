import cv2
import time

vcap = cv2.VideoCapture("rtsp://admin:admin@192.168.1.78:554/30", cv2.CAP_FFMPEG)
vcap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
vcap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)


def nothing(x):
    pass


# Khởi tạo thanh TackBars cho phép người dùng nhìn thấy và điều chỉnh giá trị
def initializeTrackbars(initializeTrackbars=0):
    cv2.namedWindow("Trackbars") # Đặt tên cho khung hiển thị
    cv2.resizeWindow("Trackbars", 500, 80) # Đặt kích thước cho khung
    cv2.createTrackbar("Threshold1", "Trackbars", 1024, 1280, nothing)
    cv2.createTrackbar("Threshold2", "Trackbars", 720, 720, nothing)


# Tạo trường hợp cho phép người dùng nhận thông số từ thanh TackBars
def valTrackbars():
    Threshold1 = cv2.getTrackbarPos("Threshold1", "Trackbars") # Để lấy giá trị hiện tại của thanh trượt.
    Threshold2 = cv2.getTrackbarPos("Threshold2", "Trackbars")
    src = Threshold1, Threshold2
    return src # Trả về 1 giá trị


initializeTrackbars()


def Image():
    while True:
        ret, frame = vcap.read()
        thres = valTrackbars()  # Gọi lại đến hàm nhận giá trị từ TaskBar
        frame = cv2.resize(frame, [thres[0], thres[1]])
        if not ret:
            print("Frame is empty")
            break
        else:
            localtime = time.localtime(time.time())
            read_time = str(localtime.tm_mday) + '-' + str(localtime.tm_mon) + '-' + str(
                localtime.tm_year) + '--' + str(localtime.tm_hour) + 'h' + str(localtime.tm_min) + 'm'
            File_name = 'CAMERA/image_' + read_time + '.jpg'
            cv2.imshow('VIDEO', frame)
            cv2.imwrite(File_name, frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

Image()