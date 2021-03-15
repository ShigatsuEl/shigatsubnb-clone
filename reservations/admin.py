from django.contrib import admin
from . import models


@admin.register(models.BookedDay)
class BookedDayAdmin(admin.ModelAdmin):

    """ BookedDay Admin Definition """

    list_display = ("day", "reservation")


@admin.register(models.Reservation)
class AdminReservation(admin.ModelAdmin):

    """ Reservation Admin Definition """

    list_display = (
        "room",
        "status",
        "check_in",
        "check_out",
        "guest",
        "in_progress",
        "is_finished",
    )

    list_filter = ("status",)

    search_fields = ("^room__name", "^guest__username")
