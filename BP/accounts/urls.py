from django.urls import path
from django.urls import path, include
from .views import home_screen_view
from accounts.views import register_view, login_view, logout_view

urlpatterns = [
    path('signup/', )
]