from django.contrib import admin

# Register your models here.
from watchlist_app.models import WatchList, StreamPlatform, Review
admin.site.register(WatchList)
admin.site.register(StreamPlatform)
admin.site.register(Review)
