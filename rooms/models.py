from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from core import models as core_models
from cal import Calendar


class AbstractItem(core_models.TimeStampModel):

    """ Abstract Item """

    name = models.CharField(_("Title"), max_length=80)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class RoomType(AbstractItem):

    """ RoomType Model Definition """

    class Meta:

        verbose_name = _("Room Type")
        verbose_name_plural = _("Room Types")
        ordering = ["name"]


class Amenity(AbstractItem):

    """ Amenity Model Definition """

    class Meta:

        verbose_name = _("Amenity")
        verbose_name_plural = _("Amenities")


class Facility(AbstractItem):

    """ Facility Model Definition """

    class Meta:

        verbose_name = _("Facility")
        verbose_name_plural = _("Facilities")


class HouseRule(AbstractItem):

    """ HouseRule Model Definition """

    class Meta:

        verbose_name = _("House Rule")
        verbose_name_plural = _("House Rules")


class Photo(core_models.TimeStampModel):

    """ Photo Model Definition """

    caption = models.CharField(_("Caption"), max_length=80)
    file = models.ImageField(_("File"), upload_to="room_photos")
    room = models.ForeignKey("Room", related_name="photos", on_delete=models.CASCADE)

    def __str__(self):
        return self.caption

    class Meta:

        verbose_name_plural = _("Photos")


class Room(core_models.TimeStampModel):

    """ Room Model Definition """

    name = models.CharField(_("Name"), max_length=140)
    description = models.TextField(
        _("Description"),
    )
    country = CountryField(
        _("Country"),
    )
    city = models.CharField(_("City"), max_length=80)
    price = models.IntegerField(
        _("Price"),
    )
    address = models.CharField(_("Address"), max_length=140)
    guests = models.IntegerField(
        _("Guest"),
    )
    beds = models.IntegerField(
        _("Bed"),
    )
    bedrooms = models.IntegerField(
        _("Bedroom"),
    )
    baths = models.IntegerField(
        _("Bath"),
    )
    check_in = models.TimeField(
        _("Check In"),
    )
    check_out = models.TimeField(
        _("Check Out"),
    )
    instant_book = models.BooleanField(_("Instant Book"), default=False)
    # Foreign Key = 일대다 관계를 가지고 있다
    # Room 어드민 패널은 User Model을 가지고 있지만 반대로 User 어드민 패널은 Room Model이 없다
    # User 어드민 패널에선 볼 수 없지만 Django가 set 필드를 주기 때문에 접근이 가능하다
    # 즉, Foreign Key로 참조하게 되면 참조된 모델도 참조한 모델을 접근할 수 있다
    # related_name -> 어떤 모델(1번째 인자)에서 접근할 때 사용되는 키워드이다(set 대신 사용)
    host = models.ForeignKey(
        "users.User",
        related_name="rooms",
        on_delete=models.CASCADE,
        verbose_name=_("Host"),
    )
    room_type = models.ForeignKey(
        "RoomType",
        related_name="rooms",
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_("Room Type"),
    )
    # Many To Many Field = 다대다 관계를 가지고 있다
    amenities = models.ManyToManyField(
        "Amenity", related_name="rooms", blank=True, verbose_name=_("Amenity")
    )
    facilities = models.ManyToManyField(
        "Facility", related_name="rooms", blank=True, verbose_name=_("Facility")
    )
    house_rules = models.ManyToManyField(
        "HouseRule", related_name="rooms", blank=True, verbose_name=_("House Rule")
    )

    def __str__(self):
        return self.name

    # 장고의 모든 모델들은 save 메서드를 가지고 있다.
    # save 메서드를 오버라이드해서 중간에 결과를 가로챈 후 부모의 save메서드를 호출할 것이다
    def save(self, *args, **kwargs):
        # 여기에서 저장하기 전에 결과를 가로채어 어떠한 작업을 한 후 super메서드를 실행
        # super 메서드로 부모의 save 메서드를 호출하여 저장작업을 한다
        self.city = str.capitalize(self.city)
        super().save(*args, **kwargs)  # Call the real save() method

    # admin 패널에서도 URL을 다루는 메서드
    def get_absolute_url(self):
        return reverse("rooms:detail", kwargs={"pk": self.pk})

    # review 수가 0이면 0값 반환 그 외는 평균점수를 반환
    def total_rating(self):
        all_reviews = self.reviews.all()
        all_rating = 0
        for review in all_reviews:
            all_rating += review.rating_average()
        if len(all_reviews) > 0:
            return round(all_rating / len(all_reviews), 2)
        else:
            return 0

    total_rating.short_description = _("Total Rating")

    def formatted(self):
        location = f"{self.city} · {self.country.name}"
        location = location if len(location) < 20 else f"{location[:20]}..."
        name = self.name if len(self.name) < 35 else f"{self.name[:35]}..."
        return {"location": location, "name": name}

    def get_first_photo(self):
        # Python은 array의 멤버를 아래와 같이 변수로 하나하나 할당하는 것이 가능하다
        # one, two, three = self.photos.all()[:1]
        # one, two, three에 각각 해당하는 배열의 인덱스를 할당할 것이다
        # 아래 식은 Array가 아닌 QuerySet이므로 작동하진 않지만 ,를 붙여주면 Python이 배열로 인식한다
        try:
            (photo,) = self.photos.all()[:1]
            return photo.file.url
        except ValueError:
            return None

    def get_four_sub_photo(self):
        photos = self.photos.all()[1:5]
        return photos

    def get_enumerate_amenity(self):
        enumerate_amenity = enumerate(self.amenities.all())
        return enumerate_amenity

    def get_amenity_count(self):
        count = self.amenities.count() - 1
        return count

    def get_enumerate_facility(self):
        enumerate_facility = enumerate(self.facilities.all())
        return enumerate_facility

    def get_facility_count(self):
        count = self.facilities.count() - 1
        return count

    def get_calendars(self):
        now = timezone.now()
        this_year = now.year
        this_month = now.month
        this_month_cal = Calendar(this_year, this_month)
        next_month_cal = Calendar(this_year, this_month + 1 if this_month != 12 else 1)
        return [this_month_cal, next_month_cal]

    class Meta:

        verbose_name_plural = _("Rooms")