from django.urls import path, include
from goods.views import makegoods


app_name = 'goods'

urlpatterns = [
    path('', makegoods, name='makegoods'),
]