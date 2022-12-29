from django.db import models
from io import *
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys

class Images(models.Model):
    user_id = models.AutoField(auto_created = True, primary_key = True)
    raw_img = models.ImageField(upload_to='raw_img',null=False)
    cvt_img = models.ImageField(upload_to='cvt_img',null=True)
