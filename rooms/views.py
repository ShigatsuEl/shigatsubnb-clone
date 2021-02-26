from math import ceil
from django.shortcuts import render
from . import models


# View 함수이름은 core/urls.py에서 사용하는 view 이름과 동일해야 한다
def all_rooms(request):
    page = request.GET.get("page", 1) or 1
    page = int(page or 1)
    size = 10
    limit = size * page
    offset = limit - size
    all_rooms = models.Room.objects.all()[offset:limit]
    page_count = ceil(models.Room.objects.count() / size)
    # 2번째 인자는 templates이름과 동일해야 한다
    return render(
        request,
        "rooms/home.html",
        context={
            "rooms": all_rooms,
            "page": page,
            "page_count": page_count,
            "page_range": range(1, page_count),
        },
    )
