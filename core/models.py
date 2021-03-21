from django.db import models
from django.utils.translation import gettext_lazy as _
from . import managers


class TimeStampModel(models.Model):

    """ Time Stamped Model """

    created = models.DateTimeField(auto_now_add=True, verbose_name=_("Created"))
    updated = models.DateTimeField(auto_now=True, verbose_name=_("Updated"))
    # 전역에서 manager를 사용하기 위함
    objects = managers.CustomModelManager()

    class Meta:
        abstract = True