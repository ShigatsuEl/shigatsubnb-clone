from django.db import models
from django.utils.translation import gettext_lazy as _
from core import models as core_models


class List(core_models.TimeStampModel):

    """ List Model Definition """

    name = models.CharField(_("Title"), max_length=80)
    user = models.OneToOneField(
        "users.User",
        related_name="list",
        on_delete=models.CASCADE,
        verbose_name=_("User"),
    )
    rooms = models.ManyToManyField(
        "rooms.Room", related_name="lists", blank=True, verbose_name=_("Room")
    )

    def __str__(self):
        return self.name

    def count_rooms(self):
        return self.rooms.count()

    count_rooms.short_description = _("Number of Rooms")
