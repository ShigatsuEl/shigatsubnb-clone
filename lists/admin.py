from django.contrib import admin
from . import models


@admin.register(models.List)
class AdminList(admin.ModelAdmin):

    """ List Admin Definition """

    list_display = ("name", "user", "count_rooms")

    search_fields = ("name",)

    # filter_horizontal = Many to Many Field속성만 가능
    filter_horizontal = ("rooms",)
