from django.contrib import admin
from .models import Experience, Perk

@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "country",
        "city",
        "price",
        "address",
        "host",
        "start_at",
        "end_at",
        "created_at",
        "updated_at",
    )
    list_filter = (
        "country",
        "city",
        "host",
        "perks",
        "created_at",
        "updated_at",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )

@admin.register(Perk)
class PerkAdmin(admin.ModelAdmin):
    
    list_display = (
        "name",
        "detail",
        "description",
        "created_at",
        "updated_at",
    )
    
    list_filter = (
        "created_at",
        "updated_at",
    )
    
    readonly_fields = (
        "created_at",
        "updated_at",
    )
    
