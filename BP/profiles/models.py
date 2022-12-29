from django.db import models
from accounts.models import Account
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE,
                                related_name='profile')
    image = models.ImageField(upload_to='profile/', default='../static/img/user.jpg', blank=True)
    message = models.TextField(max_length=300, default='자기소개를 입력해주세요!', blank=True)
    
    @property
    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        else:
            return "static/img/user.jpg"
            

@receiver(post_save, sender=Account)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=Account)
def create_user_profile(sender, instance, **kwargs):
    instance.profile.save()
    