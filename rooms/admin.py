from django.contrib import admin
from .models import Room, Amenity

@admin.action(description="Set all prices to zero")
def reset_price(modeladmin, request, rooms):
    for room in rooms.all():
        room.price = 0
        room.save()
        

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    
    actions = (
        reset_price,
        )
    list_display = (
        "name",
        "price",
        "kind",
        "total_amenities",
        "rating",
        "owner",
        "created_at",
    )
    list_filter = (
        "country",
        "city",
        "kind",
        "owner",
        "amenities",
        "created_at",
        "updated_at",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )
    search_fields = (
        "owner__username",
    )
    search_help_text = (
        "Search by username",
    )
    
    


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    
    list_display = (
        "name",
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

