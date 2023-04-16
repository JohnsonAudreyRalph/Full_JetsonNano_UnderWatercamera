from PIL import Image
from django.shortcuts import render, redirect
from django.http import StreamingHttpResponse
from django.views.decorators import gzip
from .models import Auto_cam
import os
import shutil
import glob
import cv2
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
            auto = Auto_cam(Timers=Timer, Counters=Counter, start_Time=Clock_Time, stat_Date=Clock_Date, Check_cap=False)
            auto.save()
            print("Đã lưu thông tin rồi đây")
    return redirect('index')


def Cut_Image():
    folder_path = "static/CAMERA_Temp/"
    destination_folder = "static/CAMERA"
    # Tạo thư mục đích nếu nó chưa tồn tại
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
    # Lặp qua tất cả các tệp trong thư mục nguồn
    for filename in os.listdir(folder_path):
        # Kiểm tra nếu tệp là tệp ảnh
        if filename.endswith(".jpg"):
            # Tạo đường dẫn đầy đủ cho tệp nguồn và tệp đích
            folder_file = os.path.join(folder_path, filename)
            destination_file = os.path.join(destination_folder, filename)
            # Di chuyển tệp nguồn đến tệp đích
            shutil.move(folder_file, destination_file)
    print("Đã chuyển toàn bộ file xong rồi!!!!")


def Delete_Image(folder_path):
    # tìm kiếm tất cả các file ảnh trong thư mục
    file_list = glob.glob(folder_path + '*.png') + glob.glob(folder_path + '*.jpg')
    # xóa các file ảnh trong thư mục
    for file_path in file_list:
        os.remove(file_path)
    print("Đã xóa toàn bộ ảnh")


def Camera_Auto_Cap(counters, timers):
    folder_path = "static/CAMERA_Temp/"
    destination_folder = "static/CAMERA"
    # Trước khi thực hiện chương trình. Mặc kệ có ảnh hay không. Cứ xóa hết nó đi
    Delete_Image(folder_path=folder_path)
    for i in range(counters):
        ret, frame = vcap.read()
        localtime = time.localtime(time.time())
        read_time = str(localtime.tm_hour) + 'h' + str(localtime.tm_min) + 'm' + str(i + 1)
        path_Camera = 'static/CAMERA_Temp/Image_' + read_time + '.jpg'
        cv2.imwrite(path_Camera, frame)
        files = os.listdir(folder_path)
        count = 0
        for file_name in files:
            file_path = os.path.join(folder_path, file_name)
            try:
                with Image.open(file_path) as img:
                    count += 1
            except:
                pass
        print("Số lượng ảnh trong file là: ", count)
        if count == counters:
            print('Đã đủ. Thực hiện chuyển ảnh sang thư mục chính')
            # Tạo thư mục đích nếu nó chưa tồn tại
            if not os.path.exists(destination_folder):
                os.makedirs(destination_folder)
            for filename in os.listdir(folder_path):
                # Kiểm tra nếu tệp là tệp ảnh
                if filename.endswith(".jpg"):
                    # Tạo đường dẫn đầy đủ cho tệp nguồn và tệp đích
                    folder_file = os.path.join(folder_path, filename)
                    destination_file = os.path.join(destination_folder, filename)
                    # Di chuyển tệp nguồn đến tệp đích
                    shutil.move(folder_file, destination_file)
            print("Đã chuyển toàn bộ file xong rồi!!!!")
            # Chuyển xong rồi thì xóa hết toàn bộ ảnh trong thư mục tạm thời
            Delete_Image(folder_path=folder_path)
            print("Thoát!!!!!!")
            break
        cv2.waitKey(timers * 60 * 1000)
    print('Đã xong!!!!!!')
    info = Auto_cam.objects.values()
    if info:
        queryset = Auto_cam.objects.filter(id__in=[obj['id'] for obj in info])
        for obj in queryset:
            id = obj.id
            timers = obj.Timers
            counters = obj.Counters
            time_clock = obj.start_Time
            date_clock = obj.stat_Date
            auto = Auto_cam(id=id, Timers=timers, Counters=counters, start_Time=time_clock, stat_Date=date_clock, Check_cap=True)
            auto.save()
    print("Đã đủ ảnh. Thực hiện việc khác")


def Camera_Auto(request):
    info = Auto_cam.objects.values()
    # kiểm tra biến info có tồn tại hay không
    if info:
        # info tồn tại, thực hiện các thao tác tiếp theo ở đây
        queryset = Auto_cam.objects.filter(id__in=[obj['id'] for obj in info])
        Date_now = datetime.datetime.now()
        for obj in queryset:
            # truy xuất các trường trong đối tượng
            id = obj.id
            timers = obj.Timers
            counters = obj.Counters
            time_clock = obj.start_Time
            date_clock = obj.stat_Date
            Check_CAMERA = obj.Check_cap
            # sử dụng các giá trị đó để làm gì đó
            print(f"Với {id} TIMERS: {timers}, COUNTER: {counters}, TIME: {time_clock}, DATE: {date_clock}, STATUS: {Check_CAMERA}")
            if date_clock.day == Date_now.day and date_clock.month == Date_now.month and date_clock.year == Date_now.year:
                print("Ngày đã trùng khớp, bắt đầu thực hiện so sánh với thời gian")
                if time_clock.hour == Date_now.hour and time_clock.minute == Date_now.minute:
                    print('Giờ đã trùng khớp. Thực hiện tiếp')
                    print(f"Thực hiện chụp {counters} bức ảnh, mỗi bức ảnh cách nhau {timers} phút")
                    if not Check_CAMERA:
                        Camera_Auto_Cap(counters=counters, timers=timers)
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