from django.http import Http404
from django.views.generic import ListView, DetailView, View, UpdateView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, reverse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from users import mixins as user_mixins
from . import models
from . import forms


class HomeView(ListView):

    """ HomeView Definition """

    model = models.Room
    paginate_by = 12
    paginate_orphans = 4
    ordering = "created"
    context_object_name = "rooms"


# DetailView에서 Django는 자동으로 argument가 pk인 친구를 찾기 때문에 어떤 모델의 detail인지 알 수 있다.
class RoomDetailView(DetailView):

    """ RoomDetailView Definition """

    model = models.Room


class SearchView(View):

    """ SearchView Definition """

    def get(self, request):

        country = request.GET.get("country")

        if country:

            # Bounded Form
            form = forms.SearchForm(request.GET)

            if form.is_valid():

                city = form.cleaned_data.get("city")
                country = form.cleaned_data.get("country")
                room_type = form.cleaned_data.get("room_type")
                price = form.cleaned_data.get("price")
                guests = form.cleaned_data.get("guests")
                bedrooms = form.cleaned_data.get("bedrooms")
                beds = form.cleaned_data.get("beds")
                baths = form.cleaned_data.get("baths")
                instant_book = form.cleaned_data.get("instant_book")
                superhost = form.cleaned_data.get("superhost")
                amenities = form.cleaned_data.get("amenities")
                facilities = form.cleaned_data.get("facilities")

                # filter_args = 검색 조건으로 필터링 추가
                # argument는 Model의 field__조건: 대상 으로 필터링
                filter_args = {}

                if city != "Anywhere":
                    filter_args["city__startswith"] = city

                filter_args["country"] = country

                if room_type is not None:
                    # Foreign Key를 사용해서 필터링 가능
                    filter_args["room_type"] = room_type

                if price is not None:
                    filter_args["price__lte"] = price

                if guests is not None:
                    filter_args["guests__gte"] = guests

                if bedrooms is not None:
                    filter_args["bedrooms__gte"] = bedrooms

                if beds is not None:
                    filter_args["beds__gte"] = beds

                if baths is not None:
                    filter_args["baths__gte"] = baths

                if instant_book is True:
                    filter_args["instant_book"] = True

                if superhost is True:
                    filter_args["host__superhost"] = True

                for amenity in amenities:
                    filter_args["amenities"] = amenity

                for facility in facilities:
                    filter_args["facilities"] = facility

                qs = models.Room.objects.filter(**filter_args).order_by("created")

                paginator = Paginator(qs, 10, orphans=5)

                page = request.GET.get("page", 1)

                rooms = paginator.get_page(page)

                return render(
                    request, "rooms/search.html", {"form": form, "rooms": rooms}
                )

        else:

            # Unbounded Form
            form = forms.SearchForm()

        return render(request, "rooms/search.html", {"form": form})


class EditRoomView(user_mixins.LoggedInOnlyMixin, UpdateView):

    """ EditRoomView Definition """

    model = models.Room
    template_name = "rooms/room_edit.html"
    form_class = forms.UpdateRoomForm

    # Room object를 주는 역할을 한다
    def get_object(self, queryset=None):
        room = super().get_object(queryset=queryset)
        if room.host.pk != self.request.user.pk:
            raise Http404()
        return room


class RoomPhotosView(user_mixins.LoggedInOnlyMixin, DetailView):

    """ RoomPhotosView Definition """

    model = models.Room
    template_name = "rooms/room_photos.html"

    # Room object를 주는 역할을 한다
    def get_object(self, queryset=None):
        room = super().get_object(queryset=queryset)
        if room.host.pk != self.request.user.pk:
            raise Http404()
        return room


@login_required
def delete_photo(request, room_pk, photo_pk):

    """ Delete Pohotos Definition """

    user = request.user

    try:
        room = models.Room.objects.get(pk=room_pk)
        if room.host.pk != user.pk:
            messages.error(
                request,
                "This Photo can't be deleted because you don't have permission.",
            )
        else:
            models.Photo.objects.filter(pk=photo_pk).delete()
            messages.success(request, "Photo deleted")
        return redirect(reverse("rooms:photos", kwargs={"pk": room_pk}))
    except models.Room.DoesNotExist:
        return redirect(reverse("core:home"))


class EditPhotoView(user_mixins.LoggedInOnlyMixin, SuccessMessageMixin, UpdateView):

    """ EditPhotoView Deifinition """

    model = models.Photo
    template_name = "rooms/photo_edit.html"
    # URL에 있는 pk의 이름을 찾기 위해 사용
    pk_url_kwarg = "photo_pk"
    fields = ("caption",)
    success_message = "Photo Updated"

    def get_success_url(self):
        room_pk = self.kwargs.get("room_pk")
        return reverse("rooms:photos", kwargs={"pk": room_pk})
