import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_create_hotel(client):
    url = reverse("hotel-list-create")
    payload = {"name": "Test Hotel", "address": "123 Testing Ave"}

    response = client.post(url, data=payload, content_type="application/json")

    assert response.status_code == 201
    assert "id" in response.data
    assert response.data["name"] == "Test Hotel"


@pytest.mark.django_db
def test_list_hotels(client, hotel):
    hotel("Hotel A", "Address A")
    hotel("Hotel B", "Address B")
    hotel("Hotel C", "Address C")

    url = reverse("hotel-list-create")
    response = client.get(url)

    assert response.status_code == 200
    assert len(response.data) == 3
    names = [h["name"] for h in response.data]
    assert "Hotel A" in names
    assert "Hotel B" in names
    assert "Hotel C" in names
