from django.db import models
from core.apps.auth_user.models import AbstractUser
from core.apps.auth_user.models import UserManager


# Create your models here.
class User(AbstractUser):

    objects = UserManager()

    class Meta(AbstractUser.Meta):
        db_table = 'auth_user'
        swappable = 'AUTH_USER_MODEL'
