from django import template
from lists import models as list_models

register = template.Library()


@register.simple_tag(takes_context=True)
def on_favs(context, room):
    user = context.request.user
    list = list_models.List.objects.get_or_none(user=user, name="My Favorite House")
    return room in list.rooms.all()
