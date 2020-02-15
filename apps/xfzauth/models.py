from django.contrib.auth.models import  AbstractBaseUser,PermissionsMixin,BaseUserManager
from shortuuidfield import ShortUUIDField
from  django.db import models

class UserManager(BaseUserManager):
    def _create_user(self,telephone,username,password,**kwargs):
        if not telephone:
            raise ValueError('请传入手机号码')
        if  not username:
            raise ValueError('请传入用户名')
        if not password:
            raise ValueError('请传入密码')
        user= self.model(telephone= telephone,username=username,**kwargs)
        user.set_password(password)
        user.save()
        return  user


    def create_user(self,telephone,username,password,**kwargs):
        kwargs['is_superuser'] = False
        return self._create_user(telephone,username,password,**kwargs)
    def create_superuser(self,telephone,username,password,**kwargs):
        kwargs['is_superuser'] = True
        kwargs['is_staff'] = True
        return self._create_user(telephone,username,password,**kwargs)




class User(AbstractBaseUser,PermissionsMixin):
    #我们不适用默认的自增长的主键
    #shortuuid  pip instal django-shortuuidfield
    uid = ShortUUIDField(primary_key=True)
    telephone = models.CharField(max_length=11,unique=True)
    #password = models.CharField(max_length=200)
    email = models.EmailField(unique=True,null=True)
    username = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)#建立用户自动设置时间

    USERNAME_FIELD = "telephone"
    REQUIRED_FIELDS = ['username']
    EMAIL_FIELD = 'email'
    object = UserManager()

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username