from django.contrib.auth.models import AbstractUser
from django.db import models
from sorl.thumbnail import ImageField


class Profile(AbstractUser):
    profile_pic = ImageField(upload_to='profile_pics', default='profile_pics/defaultIcon.png', blank=True, null=True)
    points = models.IntegerField(default=0)