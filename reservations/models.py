from django.db import models
from django.utils import timezone
from core import models as core_models


class BookedDay(core_models.TimeStampModel):

    """ BookDay Model Definition """

    day = models.DateField()
    reservation = models.ForeignKey("Reservation", on_delete=models.CASCADE)

    class Meta:

        verbose_name = "Booked Day"
        verbose_name_plural = "Booked Days"


class Reservation(core_models.TimeStampModel):

    """ Reservation Model Definition """

    STATUS_PENDING = "pending"
    STATUS_CONFIRMED = "confirmed"
    STATUS_CANCELED = "canceled"

    STATUS_CHOICES = (
        (STATUS_PENDING, "Pending"),
        (STATUS_CONFIRMED, "Confirmed"),
        (STATUS_CANCELED, "Canceled"),
    )

    check_in = models.DateField()
    check_out = models.DateField()
    status = models.CharField(
        max_length=12, choices=STATUS_CHOICES, default=STATUS_PENDING
    )
    guest = models.ForeignKey(
        "users.User", related_name="reservations", on_delete=models.CASCADE
    )
    room = models.ForeignKey(
        "rooms.Room", related_name="reservations", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.room} - {self.check_in}"

    def in_progress(self):
        now = timezone.now().date()
        return now >= self.check_in and now <= self.check_out

    in_progress.boolean = True

    def is_finished(self):
        now = timezone.now().date()
        return now > self.check_out

    is_finished.boolean = True

    def save(self, *args, **kwargs):
        if True:
            start = self.check_in
            end = self.check_out
            difference = end - start
            # day_range는 django range메서드로부터 사용한다
            is_existing_booked_day = BookedDay.objects.filter(
                day_range=(start, end)
            ).exists()
            if is_existing_booked_day is False:
                pass
        return super().save(*args, **kwargs)
