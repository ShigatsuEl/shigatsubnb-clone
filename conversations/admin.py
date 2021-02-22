from django.contrib import admin
from . import models


@admin.register(models.Message)
class AdminMessage(admin.ModelAdmin):

    """ Message Admin Definition """

    pass


@admin.register(models.Conversation)
class AdminConversation(admin.ModelAdmin):

    """ Conversation Admin Definition """

    pass