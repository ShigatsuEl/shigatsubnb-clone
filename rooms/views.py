from django.shortcuts import render
from django.core.paginator import Paginator
from . import models


# View 함수이름은 core/urls.py에서 사용하는 view 이름과 동일해야 한다
def all_rooms(request):
    page = request.GET.get("page", 1)
    # room_list를 선언한 것까지는 데이터베이스에서 불러오지 않기 때문에 괜찮다
    room_list = models.Room.objects.all()
    # Paginator 클래스는 첫번째 인자로 objet_list를 두번째 인자는 페이지 당 몇개의 리스트를 받는지 정함
    paginator = Paginator(room_list, 10, orphans=5)
    # get_page 메서드는 하나의 Page object를 반환
    rooms = paginator.page(int(page))
    # 2번째 인자는 templates이름과 동일해야 한다
    return render(
        request,
        "rooms/home.html",
        context={"page": rooms},
    )
