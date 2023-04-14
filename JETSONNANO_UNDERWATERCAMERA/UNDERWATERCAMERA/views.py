from django.shortcuts import render, redirect
from django.http import StreamingHttpResponse
from django.views.decorators import gzip
from asyncio import sleep
from .models import Auto_cam
import cv2
import os
import time
import webbrowser
import datetime


# vcap = cv2.VideoCapture("rtsp://admin:admin@192.168.1.78:554/30", cv2.CAP_FFMPEG)
vcap = cv2.VideoCapture(1)
vcap.set(cv2.CAP_PROP_FRAME_WIDTH, 1024)
vcap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)


def generate_frames():
    while True:
        ret, frame = vcap.read()
        if not ret:
            break
        frame = cv2.imencode('.jpg', frame)[1].tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@gzip.gzip_page
def livefe(request):
    try:
        return StreamingHttpResponse(generate_frames(), content_type="multipart/x-mixed-replace;boundary=frame")
    except:  # This is to handle when the client disconnects
        pass


def index(request):
    return render(request, 'index.html')


def Auto(request):
    if request.method == 'POST':
        Timer = request.POST['Timer']
        Counter = request.POST['Counter']
        Clock_Time = request.POST['Clock_Time']
        Clock_Date = request.POST['Clock_Date']
        print(Timer)
        if not Timer or not Counter:
            print("Thông báo: Cần nhập đầy đủ thông tin.")
        else:
            print("Nhận được đầy đủ thông tin rồi. Bắt đầu làm việc đây")
            auto = Auto_cam(Timers=Timer, Counters=Counter, start_Time=Clock_Time, stat_Date=Clock_Date)
            auto.save()
            print("Đã lưu thông tin rồi đây")
    return redirect('index')


def Camera_Auto(request):
    info = Auto_cam.objects.values()
    ret, frame = vcap.read()
    # kiểm tra biến info có tồn tại hay không
    if info:
        # info tồn tại, thực hiện các thao tác tiếp theo ở đây
        print("Thông tin nhận được: ", info)
        # print('Thông tin nhận được: ', info)
        queryset = Auto_cam.objects.filter(id__in=[obj['id'] for obj in info])
        Date_now = datetime.datetime.now()
        for obj in queryset:
            # truy xuất các trường trong đối tượng
            id = obj.id
            timers = obj.Timers
            counters = obj.Counters
            time_clock = obj.start_Time
            date_clock = obj.stat_Date
            # sử dụng các giá trị đó để làm gì đó
            print(f"Với {id} thì TIMERS là: {timers} và COUNTER là: {counters}, TIME là: {time_clock} và DATE là: {date_clock}")
            if(date_clock.day == Date_now.day and date_clock.month == Date_now.month and date_clock.year == Date_now.year):
                print("Ngày đã trùng khớp, bắt đầu thực hiện so sánh với thời gian")
                if (time_clock.hour == Date_now.hour and time_clock.minute == Date_now.minute):
                    print('Giờ đã trùng khớp. Thực hiện tiếp')
                    # Thực hiện tính thời gian TIMERS chính là khoảng thời gian timers lấy được
                    # slep = timers*60
                    # sleep(slep)
                    for i in range(counters):
                        if ret:  # nếu đọc ảnh thành công
                            localtime = time.localtime(time.time())
                            read_time = str(localtime.tm_hour) + 'h' + str(localtime.tm_min) + 'm' + str(i + 1)
                            path_Camera = 'static/CAMERA/Image_' + read_time + '.jpg'
                            cv2.imwrite(path_Camera, frame)
                        else:
                            print("Không thể đọc ảnh từ camera")
                        sleep = timers * 60000
                        cv2.waitKey(sleep)
                        # cv2.waitKey(500)  # đợi 0.5 giây để chụp ảnh tiếp theo
                    break
                else:
                    print("Thời gian không khớp. Bỏ qua")
            else:
                print("Ngày không khớp. Bỏ qua")
    else:
        # info không tồn tại hoặc rỗng, thông báo lỗi hoặc xử lý theo yêu cầu
        print("Lỗi: Không tìm thấy thông tin")
    return redirect('index')


def Open_Folder(request):
    path = 'static/CAMERA'
    print('Nhận được thông tin')
    webbrowser.open(os.path.realpath(path))
    return redirect('index')