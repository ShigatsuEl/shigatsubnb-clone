from django.contrib import admin
from django.utils.html import mark_safe
from . import models


@admin.register(models.RoomType, models.Facility, models.Amenity, models.HouseRule)
class ItemAdmin(admin.ModelAdmin):

    """ Item Admin Definition """

    list_display = ("name", "used_by")

    def used_by(self, obj):
        return obj.rooms.count()


@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):

    """ Room Admin Definition """

    # fieldsets = Model이 어떻게 보여질지 구성하는 필드
    fieldsets = (
        (
            "Basic Info",
            {"fields": ("name", "description", "country", "address", "price")},
        ),
        ("Times", {"fields": ("check_in", "check_out", "instant_book")}),
        ("Spaces", {"fields": ("guests", "beds", "bedrooms", "baths")}),
        (
            "More About the Space",
            {"fields": ("amenities", "facilities", "house_rules")},
        ),
        ("Last Details", {"fields": ("host",)}),
    )

    # list_display = 어드민 패널에서 보여지는 구성리스트
    list_display = (
        "name",
        "country",
        "city",
        "price",
        "guests",
        "beds",
        "bedrooms",
        "baths",
        "check_in",
        "check_out",
        "instant_book",
        "count_amenities",
        "count_photos",
        "total_rating",
    )

    # ordering = 자동정렬기능(앞에 오는 것이 더 빠른 순번이다)
    ordering = ("name", "price", "bedrooms")

    # list_filter = 필터링 기능
    list_filter = (
        "instant_book",
        "host__superhost",
        "city",
        "room_type",
        "amenities",
        "facilities",
        "house_rules",
        "country",
    )

    # search_fields = 검색 기능
    # (기본으로 대,소문자 구별없이 검색 가능 / ^옵션은 첫글자가 일치해야 검색 가능 / =옵션은 정확히 일치해야 검색 가능)
    search_fields = ("^city", "^host__username")

    # filter_horizontal = Many to Many Field에만 가능한 필드이다
    filter_horizontal = ("amenities", "facilities", "house_rules")

    # Custom Admin Function
    # Many to Many Field는 list가 될 수 없으므로 Custom Admin Function으로 list를 생성할 수 있다
    def count_amenities(self, obj):
        return obj.amenities.count()

    def count_photos(self, obj):
        return obj.photos.count()

    count_amenities.short_description = "Count Amenity"


@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):

    """ """

    list_display = ("__str__", "get_thumbnail")

    def get_thumbnail(self, obj):
        # Django는 우리를 해킹으로부터 지키기 위해 이러한 html형식을 막게 되어있다
        # 따라서 Django에게 이것은 안전한 문자열임을 알릴 필요가 있다
        return mark_safe(f'<img src="{obj.file.url}" width="50px" />')

    get_thumbnail.short_description = "Thumbnail"
