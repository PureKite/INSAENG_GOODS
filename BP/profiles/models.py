from django.db import models

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField('accounts.Account', on_delete=models.CASCADE,
                                related_name='profile')
    image = models.ImageField(upload_to='profile/', null=True)
    message = models.CharField(max_length=300, null=True)