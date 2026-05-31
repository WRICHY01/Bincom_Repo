from django.contrib import admin
from .models import Post, MediaItem

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "author", 
                    "date_uploaded", "updated_at"]
    search_fields = ["title", "description"]

@admin.register(MediaItem)
class MediaItemAdmin(admin.ModelAdmin):
    list_display = ["post", "media_type"]
    list_filter = ["media_type"]
