"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Divide and Conquer -> URL과 VIEW를 쪼개보자
urlpatterns = [
    path("", include("core.urls", namespace="core")),
    path("users/", include("users.urls", namespace="users")),
    path("rooms/", include("rooms.urls", namespace="rooms")),
    path("reservations/", include("reservations.urls", namespace="reservations")),
    path("admin/", admin.site.urls),
]

# DEBUG = True(개발서버)인 경우에만 실행
# settings에서 Django가 정적파일이 저장될 루트와 어느 url에서 찾을지 정해주었음
# 이제 Djnago가 파일을 우리에게 제공하기 위해 urls에서 설정할 수 있다
# static은 정적파일을 제공하는 것을 도움
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
