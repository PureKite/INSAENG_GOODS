from django.urls import path
from django.urls import path, include
# from .views import home_screen_view
from accounts.views import signup, login, logout, detail, update

app_name = 'accountsapp'

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('detail/', detail, name='detail'),
    path('update/', update, name='update')
]