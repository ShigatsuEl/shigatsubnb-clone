from django.contrib import messages
from django.shortcuts import redirect, reverse
from rooms import models as room_models
from reservations import models as reservation_models
from . import forms


def create_review(request, room, reservation):

    """ CreateReview View Definition """

    if request.method == "POST":
        form = forms.CreateReviewForm(request.POST)
        room = room_models.Room.objects.get_or_none(pk=room)
        reservation = reservation_models.Reservation.objects.get_or_none(pk=reservation)
        if not room or not reservation:
            return redirect(reverse("core:home"))
        if form.is_valid:
            if reservation.guest == request.user:
                review = form.save()
                review.room = room
                review.user = request.user
                review.save()
                messages.success(request, "Room reviewed")
                return redirect(reverse("rooms:detail", kwargs={"pk": room.pk}))
            else:
                messages.error(request, "You can't access reivew")
                return redirect(
                    reverse("reservations:detail", kwargs={"pk": reservation.pk})
                )
