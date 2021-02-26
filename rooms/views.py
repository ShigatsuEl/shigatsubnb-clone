from math import ceil
from django.shortcuts import render
from django.core.paginator import Paginator
from . import models


# View 함수이름은 core/urls.py에서 사용하는 view 이름과 동일해야 한다
def all_rooms(request):
    page = request.GET.get("page")
    room_list = models.Room.objects.all()
    paginator = Paginator(room_list, 10)
    rooms = paginator.get_page(page)
    print(vars(rooms.paginator))
    # 2번째 인자는 templates이름과 동일해야 한다
    return render(
        request,
        "rooms/home.html",
        context={"rooms": rooms},
    )
