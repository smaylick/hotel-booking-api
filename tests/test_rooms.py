import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_create_room(room_factory, hotel):
    hotel_id = hotel("My Test Hotel", "Test Address")
    room = room_factory(description="Cozy room near the sea", price="999.99", hotel_id=hotel_id)

    assert room["hotel_id"] == hotel_id
    assert "room_id" in room


@pytest.mark.django_db
def test_list_rooms(client, hotel, room_factory):
    hotel_id = hotel("List Hotel", "Listing Street")
    prices = ["100.00", "200.00", "150.00"]

    for i, price in enumerate(prices, start=1):
        room_factory(description=f"Room #{i}", price=price, hotel_id=hotel_id)

    url = reverse("room-list-create")

    response = client.get(url)
    rooms = response.json()

    assert response.status_code == 200
    assert len(rooms) == 3

    sorted_response = client.get(f"{url}?ordering=price")
    sorted_prices = [float(room["price"]) for room in sorted_response.json()]
    assert sorted_prices == sorted(sorted_prices)


@pytest.mark.django_db
def test_delete_room(client, room_factory):
    room = room_factory(description="Will be deleted soon", price="500.00")
    room_id = room["room_id"]
    url = reverse("room-destroy", kwargs={"pk": room_id})

    response = client.delete(url)
    data = response.json()

    assert response.status_code == 200
    assert data["message"] == f"Room with ID {room_id} has been deleted."

    second_response = client.delete(url)
    assert second_response.status_code == 404
