import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_create_booking(client, room_factory):
    room_data = room_factory(description="Booking test room", price="250.00")
    room_id = room_data["room_id"]

    create_url = reverse("booking-create")
    payload = {"room": room_id, "date_start": "2025-04-20", "date_end": "2025-04-22"}
    resp = client.post(create_url, data=payload, content_type="application/json")

    assert resp.status_code == status.HTTP_201_CREATED
    data = resp.json()
    assert "booking_id" in data


@pytest.mark.django_db
def test_list_bookings_for_room(client, room_factory):
    room_data = room_factory(description="List test room", price="300.00")
    room_id = room_data["room_id"]

    create_url = reverse("booking-create")
    bookings_payload = [
        {"room": room_id, "date_start": "2025-06-10", "date_end": "2025-06-12"},
        {"room": room_id, "date_start": "2025-06-15", "date_end": "2025-06-18"},
        {"room": room_id, "date_start": "2025-06-20", "date_end": "2025-06-22"},
    ]
    for p in bookings_payload:
        r = client.post(create_url, data=p, content_type="application/json")
        assert r.status_code == status.HTTP_201_CREATED

    list_url = reverse("booking-list")
    resp = client.get(f"{list_url}?room_id={room_id}")
    assert resp.status_code == status.HTTP_200_OK

    data = resp.json()
    assert len(data) == 3

    dates = [item["date_start"] for item in data]
    assert dates == sorted(dates)


@pytest.mark.django_db
def test_delete_booking(client, room_factory):
    room_data = room_factory(description="Delete booking room", price="400.00")
    room_id = room_data["room_id"]

    create_url = reverse("booking-create")
    payload = {"room": room_id, "date_start": "2025-08-10", "date_end": "2025-08-12"}
    r = client.post(create_url, data=payload, content_type="application/json")
    assert r.status_code == status.HTTP_201_CREATED
    booking_id = r.json()["booking_id"]

    delete_url = reverse("booking-destroy", kwargs={"pk": booking_id})
    del_resp = client.delete(delete_url)
    assert del_resp.status_code == status.HTTP_200_OK
    assert f"Booking with ID {booking_id} has been cancelled." in del_resp.json()["message"]

    del_resp_2 = client.delete(delete_url)
    assert del_resp_2.status_code == status.HTTP_404_NOT_FOUND
