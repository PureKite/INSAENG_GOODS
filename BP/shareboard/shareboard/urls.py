from django.urls import path
from . import views

app_name = 'shareboard'
urlpatterns = [
    path('', views.shareboard, name='shareboard'),
]