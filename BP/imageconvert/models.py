from django.db import models
from io import *
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
from django.conf import settings
from accounts.models import Account

class Images(models.Model):
    # Image_id = models.AutoField()
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    raw_img = models.ImageField(upload_to='raw_img/', null=True)
    cvt_img = models.ImageField(upload_to='cvt_img/', null=True)
