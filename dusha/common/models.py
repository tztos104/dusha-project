from django.db import models
# AbstractUser 사용
from django.contrib.auth.models import AbstractUser


# AbstractUser 상속받는 유저 클래스 생성
class User(AbstractUser):
    pass