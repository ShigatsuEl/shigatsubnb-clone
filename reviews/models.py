from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
from core import models as core_models


class Review(core_models.TimeStampModel):

    """ Review Model Definition """

    review = models.TextField(
        _("Review"),
    )
    accurancy = models.IntegerField(
        _("Accurancy"), validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    communication = models.IntegerField(
        _("Communication"), validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    cleanliness = models.IntegerField(
        _("Cleanliness"), validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    location = models.IntegerField(
        _("Location"), validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    check_in = models.IntegerField(
        _("Check In"), validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    value = models.IntegerField(
        _("Value"), validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    user = models.ForeignKey(
        "users.User",
        related_name="reviews",
        on_delete=models.CASCADE,
        verbose_name=_("User"),
    )
    room = models.ForeignKey(
        "rooms.Room",
        related_name="reviews",
        on_delete=models.CASCADE,
        verbose_name=_("Room"),
    )

    def get_review(self):
        return f"{self.review} - {self.room}"

    get_review.short_description = _("Review")

    def rating_average(self):
        avg = (
            self.accurancy
            + self.communication
            + self.cleanliness
            + self.location
            + self.check_in
            + self.value
        ) / 6
        return round(avg, 2)

    rating_average.short_description = _("AVG")

    class Meta:
        ordering = ("-created",)
