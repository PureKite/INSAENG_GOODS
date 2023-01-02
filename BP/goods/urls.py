from django.urls import path, include
from goods.views import makegoods, downloadFile


app_name = 'goods'

urlpatterns = [
    path("download/", downloadFile, name="downloadFile"),
    path('goodssample/', makegoods, name='makegoods'),
]