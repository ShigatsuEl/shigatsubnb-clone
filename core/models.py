from django.db import models
from . import managers


class TimeStampModel(models.Model):

    """ Time Stamped Model """

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # 전역에서 manager를 사용하기 위함
    objects = managers.CustomModelManager()

    class Meta:
        abstract = True