from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "kind",
        "user",
        "room",
        "experience",
        "check_in",
        "check_out",
        "expected_time",
        "guests",
        "created_at",
        "updated_at",
    )
    
    list_filter = (
        "kind",
    )
    
    readonly_fields = (
        "created_at",
        "updated_at",
    )
