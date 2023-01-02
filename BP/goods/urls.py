from django.urls import path, include
from goods.views import makegoods, downloadFile_hp, downloadFile_gr, downloadFile_kr, downloadFile_ts


app_name = 'goods'

urlpatterns = [
    path("download_hp/", downloadFile_hp, name="downloadFile_hp"),
    path("download_gr/", downloadFile_gr, name="downloadFile_gr"),
    path("download_kr/", downloadFile_kr, name="downloadFile_kr"),
    path("download_ts/", downloadFile_ts, name="downloadFile_ts"),
    path('goodssample/', makegoods, name='makegoods'),
]