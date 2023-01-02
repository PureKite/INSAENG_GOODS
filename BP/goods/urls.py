from django.urls import path, include
from goods.views import makegoods,downloadFile,autodesign


app_name = 'goods'

urlpatterns = [
    path('', autodesign, name='autodesign'),
    path("download/", downloadFile, name="downloadFile"),
    path('goodssample/', makegoods, name='makegoods'),
]