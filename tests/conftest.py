import pytest
from django.test import Client
from django.urls import reverse
from rest_framework import status


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def hotel(client):
    def _create_hotel(name="Test Hotel", address="Test Address"):
        url = reverse("hotel-list-create")
        payload = {"name": name, "address": address}
        response = client.post(url, data=payload, content_type="application/json")
        assert response.status_code == status.HTTP_201_CREATED
        return response.data["id"]

    return _create_hotel


@pytest.fixture
def room_factory(client, hotel):
    def _create_room(description="Default Room", price="1000.00", hotel_id=None):
        hotel_id = hotel_id or hotel()
        url = reverse("room-list-create")
        payload = {"hotel": hotel_id, "description": description, "price": price}
        response = client.post(url, data=payload, content_type="application/json")
        assert response.status_code == status.HTTP_201_CREATED
        return response.json()

    return _create_room
