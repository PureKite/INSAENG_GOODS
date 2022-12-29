from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'imageconvert'
urlpatterns = [
    path('viewimage', views.viewimage, name='viewimage'),
    path('download', views.downloadFile, name='downloadFile'),
    path('', views.imageconvert),
]
