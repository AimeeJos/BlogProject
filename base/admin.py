from django.contrib import admin
from .models import Room,Topic,Messages

# class RoomAdmin(admin.ModelAdmin):
#     list_display ='__dispal'

admin.site.register(Room)
admin.site.register(Topic)
admin.site.register(Messages)



