from django.contrib import admin

from .models import Tag, NewsLink, Startup

admin.site.register(NewsLink)
admin.site.register(Tag)
admin.site.register(Startup)
