from django.db import models
from django.utils import timezone
import datetime
from django.conf import settings
# Create your models here.

share_choice = [
    ('Yes', '한다'),
    ('No', '안한다'), 
]

def user_directory_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = filename.split('.')[0]
    now = datetime.datetime.now()
    filename = filename + now.strftime('%Y%m%d%H%M%S')
    filepath = 'media/article/image/'
    return filepath + filename + '.' + ext

class Post(models.Model):
    Board_id = models.AutoField(primary_key = True)
    Board_share = models.CharField(max_length=100, choices=share_choice, default='Yes')
    Board_gtype = models.CharField(max_length=100)
    Board_title = models.CharField(max_length=250)
    Board_content = models.TextField()
    Board_datetime = models.DateTimeField(default= datetime.datetime.now())
    Board_writer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class PostImage(models.Model):
    Post = models.ForeignKey('article.Post', on_delete=models.CASCADE)
    Board_image = models.ImageField(upload_to=user_directory_path)