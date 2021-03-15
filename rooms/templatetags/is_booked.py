import datetime
from django import template
from reservations import models as reservation_models

register = template.Library()


# takes_context=True시, Django가 전달해주는 user 또는 다른 context를 전달받을 수 있다
@register.simple_tag
def is_booked(room, day):
    if day.number == 0:
        return
    try:
        date = datetime.datetime(year=day.year, month=day.month, day=day.number)
        # __로 연결하는 것이 Foreign Key를 이용하는 방법이다
        reservation_models.BookedDay.objects.get(day=date, reservation__room=room)
        return True
    except reservation_models.BookedDay.DoesNotExist:
        return False