from django.urls import path

from .views import (
    BookingCreateAPIView,
    BookingDestroyAPIView,
    BookingListAPIView,
    HotelListCreateAPIView,
    RoomDestroyAPIView,
    RoomListCreateAPIView,
)

urlpatterns = [
    path("", HotelListCreateAPIView.as_view(), name="hotel-list-create"),
    path("rooms/", RoomListCreateAPIView.as_view(), name="room-list-create"),
    path("rooms/<int:pk>/", RoomDestroyAPIView.as_view(), name="room-destroy"),
    path("bookings/create/", BookingCreateAPIView.as_view(), name="booking-create"),
    path("bookings/<int:pk>/", BookingDestroyAPIView.as_view(), name="booking-destroy"),
    path("bookings/list/", BookingListAPIView.as_view(), name="booking-list"),
]
