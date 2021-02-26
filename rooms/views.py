from django.shortcuts import render
from . import models


# View 함수이름은 core/urls.py에서 사용하는 view 이름과 동일해야 한다
def all_rooms(request):
    all_rooms = models.Room.objects.all()
    # 2번째 인자는 templates이름과 동일해야 한다
    return render(request, "rooms/home.html", context={"rooms": all_rooms})
