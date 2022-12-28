from django.urls import path
from loading.views import loading

app_name = 'loading'

urlpatterns = [
    path('', loading, name='loading'),
]