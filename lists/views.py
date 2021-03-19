from django.shortcuts import redirect, reverse
from django.views.generic import TemplateView
from rooms import models as room_models
from . import models


def toggle_room(request, room_pk):

    """ ToggleRoom View Deifinition """

    action = request.GET.get("action", None)
    room = room_models.Room.objects.get_or_none(pk=room_pk)
    if room is not None and action is not None:
        the_list, created = models.List.objects.get_or_create(
            user=request.user, name="My Favorite House"
        )
        if action == "add":
            # Many To Many Field를 추가할 때 add 메서드 사용
            the_list.rooms.add(room)
        elif action == "remove":
            the_list.rooms.remove(room)
    return redirect(reverse("rooms:detail", kwargs={"pk": room_pk}))


class SeeFavsView(TemplateView):

    """ SeeFavs View Definition """

    template_name = "lists/detail.html"
