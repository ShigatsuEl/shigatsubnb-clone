from django.urls import path
from rooms import views as room_views

# core와 관련된 URL 라우트와 VIEW 처리이다
app_name = "core"

urlpatterns = [
    path("", room_views.HomeView.as_view(), name="home"),
]