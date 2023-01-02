from django.db import models
from django.conf import settings

# Create your models here.

# 1. User(외래키)
# 2. 핸드폰케이스 도안(상대)
# 3. 그립톡
# 4. 키링 도안(상대)
# 5. 티셔츠 도안

class design(models.Model):
    design_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    design_hp = models.ImageField(upload_to='goods/image/')
    design_gr = models.ImageField(upload_to='goods/image/')
    design_kr = models.ImageField(upload_to='goods/image/')
    design_ts = models.ImageField(upload_to='goods/image/')