from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('video_feed/', livefe, name='video_feed'),
    path('Auto/', Auto, name='Auto'),
    path('Camera_Auto/', Camera_Auto, name='Camera_Auto'),
    path('Open_Folder/', Open_Folder, name='Open_Folder')
]