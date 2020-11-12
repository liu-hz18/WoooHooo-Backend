from django.contrib import admin

from .models import User, SearchHistory, BrowseHistory, KeyWord

# Register your models here.
admin.site.register(User)
admin.site.register(SearchHistory)
admin.site.register(BrowseHistory)
admin.site.register(KeyWord)
