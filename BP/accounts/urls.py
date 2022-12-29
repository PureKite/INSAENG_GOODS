from django.urls import path
from django.urls import path, include
# from .views import home_screen_view
from accounts.views import signup, login, logout, detail, update, password_change, delete

app_name = 'accountsapp'

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('detail/<int:pk>/', detail, name='detail'),
    path('update/<int:pk>/', update, name='update'),
    path('delete/', delete, name='delete'),
    path('password/<int:pk>', password_change, name='password'),
]