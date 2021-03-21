from django.contrib import admin
from . import models


@admin.register(models.Conversation)
class AdminConversation(admin.ModelAdmin):

    """ Conversation Admin Definition """

    # __str__메서드는 Message Model Class가 생성될 때 자동으로 호출
    # list_display 인자가 없다면 __str__메서드는 자동으로 호출되지만 여러개라면 아래와 같이 호출
    # __str__ -> get_conversation
    list_display = ("get_conversation", "count_messages", "count_participants")


@admin.register(models.Message)
class AdminMessage(admin.ModelAdmin):

    """ Message Admin Definition """

    list_display = ("__str__", "created")
