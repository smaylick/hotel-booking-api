from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import filters, generics, status
from rest_framework.response import Response

from . import serializers
from .models import Booking, Hotel, Room


class HotelListCreateAPIView(generics.ListCreateAPIView):
    queryset = Hotel.objects.all()
    serializer_class = serializers.HotelSerializer


class RoomListCreateAPIView(generics.ListCreateAPIView):
    queryset = Room.objects.all()
    serializer_class = serializers.RoomSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["price", "created_at"]
    ordering = ["-created_at"]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        room_id = response.data["id"]
        hotel_id = response.data["hotel"]
        return Response(
            {"room_id": room_id, "hotel_id": hotel_id}, status=status.HTTP_201_CREATED
        )


class RoomDestroyAPIView(generics.DestroyAPIView):
    queryset = Room.objects.all()
    serializer_class = serializers.RoomSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        room_id = instance.id
        self.perform_destroy(instance)
        return Response(
            {"message": f"Room with ID {room_id} has been deleted."},
            status=status.HTTP_200_OK,
        )


class BookingCreateAPIView(generics.CreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = serializers.BookingSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        booking_id = response.data["id"]
        return Response({"booking_id": booking_id}, status=status.HTTP_201_CREATED)


class BookingDestroyAPIView(generics.DestroyAPIView):
    queryset = Booking.objects.all()
    serializer_class = serializers.BookingSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        booking_id = instance.id
        self.perform_destroy(instance)
        return Response(
            {"message": f"Booking with ID {booking_id} has been cancelled."},
            status=status.HTTP_200_OK,
        )


@extend_schema(
    parameters=[
        OpenApiParameter(
            name="room_id",
            required=False,
            type=int,
            description="ID номера, для которого нужно получить бронирования",
        ),
    ]
)
class BookingListAPIView(generics.ListAPIView):
    serializer_class = serializers.BookingSerializer

    def get_queryset(self):
        room_id = self.request.query_params.get("room_id")
        if room_id is not None:
            return Booking.objects.filter(room_id=room_id)
        return Booking.objects.all()
