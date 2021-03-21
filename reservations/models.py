import datetime
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from core import models as core_models


class BookedDay(core_models.TimeStampModel):

    """ BookDay Model Definition """

    day = models.DateField(_("Day"))
    reservation = models.ForeignKey(
        "Reservation", on_delete=models.CASCADE, verbose_name=_("Reservation")
    )

    class Meta:

        verbose_name = "Booked Day"
        verbose_name_plural = _("Booked Days")


class Reservation(core_models.TimeStampModel):

    """ Reservation Model Definition """

    STATUS_PENDING = "pending"
    STATUS_CONFIRMED = "confirmed"
    STATUS_CANCELED = "canceled"

    STATUS_CHOICES = (
        (STATUS_PENDING, _("Pending")),
        (STATUS_CONFIRMED, _("Confirmed")),
        (STATUS_CANCELED, _("Canceled")),
    )

    check_in = models.DateField(_("Check In"))
    check_out = models.DateField(_("Check Out"))
    status = models.CharField(
        _("Status"), max_length=12, choices=STATUS_CHOICES, default=STATUS_PENDING
    )
    guest = models.ForeignKey(
        "users.User",
        related_name="reservations",
        on_delete=models.CASCADE,
        verbose_name=_("Guest"),
    )
    room = models.ForeignKey(
        "rooms.Room",
        related_name="reservations",
        on_delete=models.CASCADE,
        verbose_name=_("Room"),
    )

    def __str__(self):
        return f"{self.room} - {self.check_in}"

    def in_progress(self):
        now = timezone.now().date()
        return now >= self.check_in and now <= self.check_out

    in_progress.boolean = True
    in_progress.short_description = _("In Progress")

    def is_finished(self):
        now = timezone.now().date()
        is_finished = now > self.check_out
        if is_finished:
            BookedDay.objects.filter(reservation=self).delete()
        return is_finished

    is_finished.boolean = True
    is_finished.short_description = _("Is Finished")

    def save(self, *args, **kwargs):
        if self.pk is None:
            start = self.check_in
            end = self.check_out
            difference = end - start
            # field__range는 django range메서드로부터 사용한다
            is_existing_booked_day = BookedDay.objects.filter(
                day__range=(start, end)
            ).exists()
            if not is_existing_booked_day:
                # 여기서 Reservation을 save하는 이유는 Reservation이 존재해야 BookdedDay를 저장 가능케 하기 위함
                super().save(*args, **kwargs)
                for i in range(difference.days + 1):
                    day = start + datetime.timedelta(days=i)
                    BookedDay.objects.create(day=day, reservation=self)
                    return
        return super().save(*args, **kwargs)

    class Meta:

        ordering = ["-status"]
        verbose_name_plural = _("Reservations")
