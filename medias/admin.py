from django.contrib import admin
from .models import Photo, Video

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = (
        "room",
        "experience",
        "description",
        "created_at",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )
    
@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = (
        "experience",
        "created_at",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )
