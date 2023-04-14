from PIL import Image
from flask import Flask, render_template, Response, redirect, url_for
import cv2
import time
import os

app = Flask(__name__)

vcap = cv2.VideoCapture("rtsp://admin:admin@192.168.1.78:554/30", cv2.CAP_FFMPEG)
vcap.set(cv2.CAP_PROP_FRAME_WIDTH, 1024)
vcap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)


def Count():
    folder_path = "CAMERA/"
    count = 0
    files = os.listdir(folder_path)
    for file_name in files:
        file_path = os.path.join(folder_path, file_name)
        try:
            with Image.open(file_path) as img:
                count += 1
        except:
            pass
    print("Số lượng ảnh trong file là: ", count)


def generate_frames():
    while True:
        ret, frame = vcap.read()
        if not ret:
            break
        frame = cv2.imencode('.jpg', frame)[1].tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/capture')
def capture():
    ret, frame = vcap.read()
    localtime = time.localtime(time.time())
    read_time = str(localtime.tm_mday) + '-' + str(localtime.tm_mon) + '-' + str(
                localtime.tm_year) + '--' + str(localtime.tm_hour) + 'h' + str(localtime.tm_min) + 'm' + str(localtime.tm_sec) + 's'
    file_name = 'CAMERA/image_' + read_time + '.jpg'
    cv2.imwrite(file_name, frame)
    Count()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)