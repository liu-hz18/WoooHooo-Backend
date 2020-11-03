from django.contrib import admin

from .models import User, SearchHistory, BrowseHistory

# Register your models here.
admin.site.register(User)
admin.site.register(SearchHistory)
admin.site.register(BrowseHistory)
