from django.db import models
from django.utils import timezone
import datetime
# Create your models here.

share_choice = [
    ('Yes', '한다'),
    ('no', '안한다'), 
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
    Board_share = models.CharField(max_length=100, choices=share_choice)
    Board_gtype = models.CharField(max_length=100)
    Board_title = models.CharField(max_length=250)
    Board_content = models.TextField()
    Board_datetime = models.DateTimeField(default= datetime.datetime.now())
    
    # def get_absolute_url(self): # redirect시 활용
    #     return reverse('myapp:post_detail', args=[self.id])

class PostImage(models.Model):
    Post = models.ForeignKey('article.Post', on_delete=models.CASCADE)
    # Image_id = models.IntegerField(default=0)
    Board_image = models.ImageField(upload_to=user_directory_path)