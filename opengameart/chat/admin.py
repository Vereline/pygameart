from django.contrib import admin
from chat.models import Message
# Register your models here.


class MessageAdmin(admin.ModelAdmin):
    model = Message
    list_display = ('sender', 'receiver', 'id', 'timestamp', 'is_read')


admin.site.register(Message, MessageAdmin)
