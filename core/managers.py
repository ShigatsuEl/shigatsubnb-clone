from django.db import models
from django.contrib.auth.models import UserManager


# models.blabla.objects.get ..filter ..crete 등을 manager라고 정의한다
# manager를 만드는 것도 가능하며 manager.py에 정의한다
class CustomModelManager(models.Manager):
    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except self.model.DoesNotExist:
            return None


class CustomUserManager(CustomModelManager, UserManager):
    pass