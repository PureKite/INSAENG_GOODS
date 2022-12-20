from django.urls import path

from . import views

app_name = 'article'

urlpatterns = [
    path('create/', views.CreatePost, name='CreatePost'),
    path('detail/<int:postid>', views.DetailPost, name='DetailPost'),
    path('delete/<int:postid>', views.DeletePost, name='DeletePost'),
    path('update/<int:postid>', views.UpdatePost, name='UpdatePost'),
    path('listpost/', views.ListPost, name='ListPost'),
]