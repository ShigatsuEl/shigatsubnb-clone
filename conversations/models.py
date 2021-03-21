from django.db import models
from django.utils.translation import gettext_lazy as _
from core import models as core_models


class Conversation(core_models.TimeStampModel):

    """ Conversation Model Definition """

    class Meta:

        verbose_name = _("Conversation")
        verbose_name_plural = _("Conversations")

    participants = models.ManyToManyField(
        "users.User",
        related_name="conversations",
        blank=True,
        verbose_name=_("Participant"),
    )

    # __str__메서드는 str을 반환한다
    # 따라서 return 값은 리스트가 아니라 join메서드를 사용한 문자열을 반환한다
    def __str__(self):
        usernames = []
        for user in self.participants.all():
            usernames.append(user.username)
        return ", ".join(usernames)

    def count_messages(self):
        return self.messages.count()

    count_messages.short_description = _("Number of Messages")

    def count_participants(self):
        return self.participants.count()

    count_participants.short_description = _("Number of Participants")


class Message(core_models.TimeStampModel):

    """ Message Model Definition """

    class Meta:

        verbose_name = _("Message")
        verbose_name_plural = _("Messages")

    message = models.TextField(_("Message"))
    user = models.ForeignKey(
        "users.User",
        related_name="messages",
        on_delete=models.CASCADE,
        verbose_name=_("User"),
    )
    conversation = models.ForeignKey(
        "Conversation",
        related_name="messages",
        on_delete=models.CASCADE,
        verbose_name=_("Conversation"),
    )

    def __str__(self):
        return f"{self.user} says: {self.message}"
