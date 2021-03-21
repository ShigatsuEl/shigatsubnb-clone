from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from rooms import models as room_models
from . import models


class RoomInline(admin.TabularInline):

    """ RoomInline Admin Definition """

    model = room_models.Room


@admin.register(models.User)
class CustomUserAdmin(UserAdmin):

    """ Custom User Admin """

    # Room Admin 패널을 가져올 수 있다
    inlines = (RoomInline,)

    fieldsets = UserAdmin.fieldsets + (
        (
            _("Custom Profile"),
            {
                "fields": (
                    "avatar",
                    "gender",
                    "bio",
                    "birthdate",
                    "language",
                    "currency",
                    "superhost",
                    "login_method",
                )
            },
        ),
    )

    list_display = (
        "username",
        "first_name",
        "last_name",
        "email",
        "is_active",
        "language",
        "currency",
        "superhost",
        "is_staff",
        "is_superuser",
        "email_verified",
        "email_secret",
        "login_method",
    )

    list_filter = UserAdmin.list_filter + ("superhost",)
