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
    room_types = models.RoomType.objects.all()
    return render(
        requset,
        "rooms/search.html",
        {"city": city, "countries": countries, "room_types": room_types},
    )
