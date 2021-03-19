from django.db.models import Q
from django.shortcuts import redirect, reverse
from django.views.generic import DetailView
from users import models as user_models
from . import models


def go_conversation(request, host_pk, guest_pk):
    host = user_models.User.objects.get_or_none(pk=host_pk)
    guest = user_models.User.objects.get_or_none(pk=guest_pk)
    if host is not None and guest is not None:
        try:
            conversation = models.Conversation.objects.get(
                # filter로 걸러내기 어려운 쿼리를 할 때만 사용한다
                Q(participants=host)
                & Q(participants=guest)
            )
        except models.Conversation.DoesNotExist:
            conversation = models.Conversation.objects.create()
            conversation.participants.add(host, guest)
        return redirect(reverse("conversations:detail", kwargs={"pk": conversation.pk}))


class ConversationDetailView(DetailView):

    """ ConversationDetail View Definition """

    model = models.Conversation
    template_name = "conversations/detail.html"
