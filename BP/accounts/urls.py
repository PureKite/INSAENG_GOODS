from django.urls import path
from django.urls import path, include
# from .views import home_screen_view
from accounts.views import signup_view, login_view, logout_view

app_name = 'accountsapp'

urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]