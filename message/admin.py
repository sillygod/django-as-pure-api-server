from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import Message


class MessageAdmin(admin.ModelAdmin):

    list_display = ('id', 'user', 'subject', 'message', 'created_at')


admin.site.register(Message, MessageAdmin)
