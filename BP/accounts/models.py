from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
 
class MyAccountManager(BaseUserManager):
    # 일반 user 생성, username 이 userID를 의미함
    def create_user(self, username, name, nickname, email, password=None):
        if not username:
            raise ValueError("Users must have an userID.")
        if not name:
            raise ValueError("Users must have a name.")
        if not nickname:
            raise ValueError('Users must have a nickname.')
        if not email:
            raise ValueError("Users must have an email address.")


        user = self.model(
            username = username,
            name = name,
            nickname = nickname,            
            email = self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
 
    # 관리자 User 생성
    def create_superuser(self, username, name, nickname, email, password):
        user = self.create_user(
            username = username,
            name = name,
            nickname = nickname,            
            email = self.normalize_email(email),
            password=password
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
 
class Account(AbstractBaseUser):
    username    = models.CharField(max_length=30, unique=True)
    name        = models.CharField(max_length=40, null=False, blank=False)    
    nickname    = models.CharField(max_length=30, unique=False)
    email       = models.EmailField(verbose_name='email', max_length=60, unique=True)
    create_at   = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login  = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin    = models.BooleanField(default=False)
    is_active   = models.BooleanField(default=True)
    is_staff    = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
 
    objects = MyAccountManager()  # 헬퍼 클래스 사용
 
    USERNAME_FIELD = 'username'  # 로그인 ID로 사용할 필드
    REQUIRED_FIELDS = ['name', 'nickname', 'email'] # 필수 작성 필드
 
    def __str__(self):
        return self.username
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
 
    def has_module_perms(self, app_lable):
        return True