import os
import json
import requests
import datetime

tokens = "ya29.a0Ael9sCNIpWxQYoPYdKoJs3MNKnjMs3tvURGScT23zaHXxK4MvJxNlaeEg8QLWl588n22lbaWUZeJTTvBzpd014qNms87CTGCHjqmsiQkKIv7omnd92K86XQB5oyQP70e6sAIdUjwZoWrCnnTnSzeee-Q4MD-aCgYKARMSARESFQF4udJhMatRBg0q5kXKhDyCXJkSxQ0163"
id_Folder_Drive = "1pakUJ7KruePuudKxDSxWW7BzH1GOpcIS"
path_Folder = "TEST"

def UploadImageDrive():
    # Thực hiện thiết lập quyền cho phép truy cập vào Google Drive
    headers = {
        "Authorization": "Bearer " + tokens
    }
    # Lấy thời gian ngày hôm nay
    now = datetime.datetime.now()
    # Định dạng chuỗi ngày tháng theo định dạng "dd-mm-yyyy"
    date_string = now.strftime("%d-%m-%Y")
    # Thực hiện thiết lập địa chỉ thư mục gửi lên trên Google Drive
    folder_metadata = {
        "name": date_string,
        "parents": [id_Folder_Drive],
        "mimeType": "application/vnd.google-apps.folder"
    }
    # Tạo thư mục trong Google Drive
    r = requests.post(
        "https://www.googleapis.com/drive/v3/files",
        headers=headers,
        json=folder_metadata
    )

    folder_id = r.json()["id"]
    # Lấy danh sách các tệp trong thư mục
    files = os.listdir(path_Folder)

    # Lặp qua danh sách các tệp và thực hiện tải từng tệp lên Google Drive
    for file_name in files:
        file_metadata = {
            "name": file_name,
            "parents": [folder_id]
        }
        files = {
            "data": ("metadata", json.dumps(file_metadata), "application/json;charset=UTF-8"),
            "file": open(path_Folder + "/" + file_name, "rb")
        }
        r = requests.post(
            "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart",
            headers=headers,
            files=files
        )
        # Phân tích cú pháp JSON của phản hồi
        response_data = json.loads(r.text)
        # Lấy tên của tệp đã tải lên
        uploaded_file_name = response_data.get("name")
        print('==> Tệp đã tải lên là: ', uploaded_file_name)
    print('Đã thực hiện tải xong')

UploadImageDrive()