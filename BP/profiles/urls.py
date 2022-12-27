from django.urls import path
from profiles.views import update, mydesign

app_name = 'profilesapp'

urlpatterns = [
    path('update/<int:pk>/', update, name='update'),
    path('mydesign/', mydesign, name='mydesign'),
]