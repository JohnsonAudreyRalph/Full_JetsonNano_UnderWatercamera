import cv2
import time

vcap = cv2.VideoCapture("rtsp://admin:admin@192.168.1.84:554/30", cv2.CAP_FFMPEG)

vcap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
vcap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)


def Image():
    while True:
        ret, frame = vcap.read()
        frame = cv2.resize(frame, [1024, 720])
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
