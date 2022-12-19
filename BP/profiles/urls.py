from django.urls import path
from profiles.views import update

app_name = 'profilesapp'

urlpatterns = [
    path('update/<int:pk>', update, name='update'),
]