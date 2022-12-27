from django.urls import path

from . import views

app_name = 'articleapp'

urlpatterns = [
    path('create/', views.CreatePost, name='CreatePost'),
    path('detail/<int:postid>', views.DetailPost, name='DetailPost'),
    path('delete/<int:postid>', views.DeletePost, name='DeletePost'),
    path('update/<int:postid>', views.UpdatePost, name='UpdatePost'),
    path('createcomment/<int:postid>', views.CreateComment, name='CreateComment'),
    path('updatecomment/', views.UpdateComment, name='UpdateComment'),
    path('deletecomment/<int:postid>/<int:commentid>', views.DeleteComment, name='DeleteComment'),
    path('', views.ListPost, name='ListPost'),
]