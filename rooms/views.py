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
    city = requset.GET.get("city", "Anywhere")
    city = str.capitalize(city)
    country = requset.GET.get("country", "KR")
    room_type = int(requset.GET.get("room_type", 0))
    price = int(requset.GET.get("price", 0))
    guests = int(requset.GET.get("guests", 0))
    bedrooms = int(requset.GET.get("bedrooms", 0))
    beds = int(requset.GET.get("beds", 0))
    baths = int(requset.GET.get("baths", 0))
    select_amenities = requset.GET.get("amenities")
    select_facilities = requset.GET.get("facilities")
    print(select_amenities, select_facilities)

    form = {
        "city": city,
        "select_room_type": room_type,
        "select_country": country,
        "price": price,
        "guests": guests,
        "bedrooms": bedrooms,
        "beds": beds,
        "baths": baths,
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

    return render(requset, "rooms/search.html", {**form, **choices})
