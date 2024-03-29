from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("", views.Rooms.as_view()),
    path("<int:pk>/", views.RoomDetail.as_view()),
    path("<int:pk>/reviews", views.RoomReviews.as_view()),
    path("<int:pk>/photos", views.RoomPhotos.as_view()),
    path("amenities/", views.Amenities.as_view()),
    path("amenities/<int:pk>/", views.AmenitiyDetail.as_view())
]

