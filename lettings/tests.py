import pytest
from django.urls import resolve, reverse

from . import views
from .models import Address, Letting


def test_address_display_formats_number_then_street():
    address = Address(number=42, street="Palm Street")

    assert str(address) == "42 Palm Street"


@pytest.mark.django_db
def test_letting_detail_page_shows_letting_title(client):
    address = Address.objects.create(
        number=42,
        street="Palm Street",
        city="Irvine",
        state="CA",
        zip_code=92602,
        country_iso_code="USA",
    )
    letting = Letting.objects.create(title="Ocean View", address=address)

    response = client.get(f"/lettings/{letting.id}/")

    assert response.status_code == 200
    assert b"Ocean View" in response.content


@pytest.mark.django_db
def test_letting_detail_page_returns_not_found(client):
    highest_id = Letting.objects.order_by("-pk").values_list("pk", flat=True).first()
    missing_id = (highest_id or 0) + 1

    response = client.get(f"/lettings/{missing_id}/")

    assert response.status_code == 404


def test_lettings_detail_url_reverses_to_detail_path():
    assert reverse("lettings:letting", args=[7]) == "/lettings/7/"


def test_lettings_detail_url_resolves_to_letting_view():
    match = resolve("/lettings/7/")

    assert match.func is views.letting
    assert match.kwargs == {"letting_id": 7}
