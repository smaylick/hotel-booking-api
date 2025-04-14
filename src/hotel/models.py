from django.db import models


class Hotel(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Room(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name="rooms")
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.hotel.name} – Room #{self.pk} ({self.price}₽)"


class Booking(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="bookings")
    date_start = models.DateField()
    date_end = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["date_start"]
        indexes = [
            models.Index(fields=["room"]),
            models.Index(fields=["date_start"]),
        ]
        unique_together = ("room", "date_start", "date_end")

    def __str__(self):
        return f"Booking #{self.pk} – Room {self.room.pk} ({self.date_start} → {self.date_end})"
