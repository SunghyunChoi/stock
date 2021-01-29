from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.contrib.auth.models import PermissionsMixin, BaseUserManager
from django.conf import settings
# 관심 기업/ 정보/ 닉네임 /돈 저장하기 위한 모델
# Create your models here.


class UserInfo(models.Model):

    user_ID = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    company = models.CharField(max_length=50)
    field = models.CharField(max_length=50)
    nickname = models.CharField(max_length=50)
    cash = models.IntegerField(default='10000000')


class MyUserManager(BaseUserManager):
    def create_user(self, username, email, nickname=None, company=None, field=None, cash=10000000, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=MyUserManager.normalize_email(email),
            nickname=nickname,
            company=company,
            field=field,
            cash=cash,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nickname, password):
        u = self.create_user(email=email,
                             nickname=nickname,
                             password=password,
                             )
        u.is_admin = True
        u.save(using=self._db)
        return u

class MyUser(AbstractUser):

    company = models.CharField(max_length=50)
    field = models.CharField(max_length=50)
    nickname = models.CharField(max_length=50)
    cash = models.IntegerField(default='10000000')