from django.views.generic import ListView, DetailView
from django.shortcuts import render
from django_countries import countries
from . import models


class HomeView(ListView):

    """ HomeView Definition """

    model = models.Room
    paginate_by = 10
    paginate_orphans = 5
    ordering = "created"
    context_object_name = "rooms"


# DetailView에서 Django는 자동으로 argument가 pk인 친구를 찾기 때문에 어떤 모델의 detail인지 알 수 있다.
class RoomDetailView(DetailView):

    """ RoomDetailView Definition """

    model = models.Room


def search(requset):
    # URL에서 가져오는 쿼리들은 대부분 str타입이기 때문에 변형해줘야 한다
    city = requset.GET.get("city", "Anywhere")
    city = str.capitalize(city)
    country = requset.GET.get("country", "KR")
    room_type = int(requset.GET.get("room_type", 0))
    price = int(requset.GET.get("price", 0))
    guests = int(requset.GET.get("guests", 0))
    bedrooms = int(requset.GET.get("bedrooms", 0))
    beds = int(requset.GET.get("beds", 0))
    baths = int(requset.GET.get("baths", 0))
    select_amenities = requset.GET.getlist("amenities")
    select_facilities = requset.GET.getlist("facilities")
    instant_book = bool(requset.GET.get("instant_book", False))
    superhost = bool(requset.GET.get("superhost", False))

    form = {
        "city": city,
        "select_room_type": room_type,
        "select_country": country,
        "price": price,
        "guests": guests,
        "bedrooms": bedrooms,
        "beds": beds,
        "baths": baths,
        "select_amenities": select_amenities,
        "select_facilities": select_facilities,
        "instant_book": instant_book,
        "superhost": superhost,
    }

    room_types = models.RoomType.objects.all()
    amenities = models.Amenity.objects.all()
    facilities = models.Facility.objects.all()

    choices = {
        "countries": countries,
        "room_types": room_types,
        "amenities": amenities,
        "facilities": facilities,
    }

    # filter_args = 검색 조건으로 필터링 추가
    # argument는 Model의 field__조건: 대상 으로 필터링
    filter_args = {}

    if city != "Anywhere":
        filter_args["city__startswith"] = city

    filter_args["country"] = country

    if room_type != 0:
        # Foreign Key를 사용해서 필터링 가능
        filter_args["room_type__pk"] = room_type

    if price != 0:
        filter_args["price__lte"] = price

    if guests != 0:
        filter_args["guests__gte"] = guests

    if bedrooms != 0:
        filter_args["bedrooms__gte"] = bedrooms

    if beds != 0:
        filter_args["beds__gte"] = beds

    if baths != 0:
        filter_args["baths__gte"] = baths

    print(instant_book, superhost)

    if instant_book is True:
        filter_args["instant_book"] = True

    if superhost is True:
        filter_args["host__superhost"] = True

    if len(select_amenities) > 0:
        for select_amenity in select_amenities:
            filter_args["amenities__pk"] = int(select_amenity)

    if len(select_facilities) > 0:
        for select_facility in select_facilities:
            filter_args["facilities__pk"] = int(select_facility)

    rooms = models.Room.objects.filter(**filter_args)

    return render(requset, "rooms/search.html", {**form, **choices, "rooms": rooms})
