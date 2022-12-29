from django.urls import path, include
from goods.views import makegoods,downloadFile


app_name = 'goods'

urlpatterns = [
    path('', makegoods, name='makegoods'),
    path("download/", downloadFile, name="downloadFile"),
]