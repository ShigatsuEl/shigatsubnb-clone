from django.shortcuts import render
from . import models


# View 함수이름은 core/urls.py에서 사용하는 view 이름과 동일해야 한다
def all_rooms(request):
    page = int(request.GET.get("page", 1))
    size = 10
    limit = size * page
    offset = limit - size
    all_rooms = models.Room.objects.all()[offset:limit]
    # 2번째 인자는 templates이름과 동일해야 한다
    return render(request, "rooms/home.html", context={"rooms": all_rooms})
