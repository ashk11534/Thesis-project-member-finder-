from django.contrib import admin
from .models import User, University, Tag, Room, RoomMessage, UserMessage

# Register your models here.

admin.site.register(User)
admin.site.register(University)
admin.site.register(Tag)
admin.site.register(Room)
admin.site.register(RoomMessage)
admin.site.register(UserMessage)