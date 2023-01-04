from django.db import models
from django.utils import timezone
import datetime
from django.conf import settings
from django.urls import reverse
import os
# Create your models here.

share_choice = [
    ('희망', '희망'),
    ('비희망', '비희망'), 
]

def user_directory_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = filename.split('.')[0]
    now = datetime.datetime.now()
    filename = filename + now.strftime('%Y%m%d%H%M%S')
    filepath = 'article/image/'
    return filepath + filename + '.' + ext

class Post(models.Model):
    Board_id = models.AutoField(primary_key = True)
    Board_share = models.CharField(max_length=100, choices=share_choice, default='희망')
    Board_gtype = models.CharField(max_length=100)
    Board_title = models.CharField(max_length=250)
    Board_content = models.TextField()
    Board_datetime = models.DateTimeField(default=timezone.now)
    Board_writer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)

class PostImage(models.Model):
    Post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='postimage')
    Board_image = models.ImageField(upload_to=user_directory_path)
    
class Comment(models.Model):
    Comment_post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    Comment_content = models.CharField(max_length=200)
    Comment_writer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    Comment_datetime = models.DateTimeField(auto_now=True)