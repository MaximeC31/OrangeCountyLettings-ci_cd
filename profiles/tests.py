import pytest
from django.contrib.auth.models import User
from django.urls import resolve, reverse

from . import views
from .models import Profile


def test_profile_display_returns_username():
    profile = Profile(user=User(username="alice"))

    assert str(profile) == "alice"


@pytest.mark.django_db
def test_profile_detail_page_shows_profile_username(client):
    user = User.objects.create_user(username="alice")
    Profile.objects.create(user=user, favorite_city="Irvine")

    response = client.get("/profiles/alice/")

    assert response.status_code == 200
    assert b"alice" in response.content


@pytest.mark.django_db
def test_profile_detail_page_returns_not_found(client):
    missing_username = f"missing-profile-{User.objects.count()}"

    response = client.get(f"/profiles/{missing_username}/")

    assert response.status_code == 404


def test_profiles_detail_url_reverses_to_detail_path():
    assert reverse("profiles:profile", args=["alice"]) == "/profiles/alice/"


def test_profiles_detail_url_resolves_to_profile_view():
    match = resolve("/profiles/alice/")

    assert match.func is views.profile
    assert match.kwargs == {"username": "alice"}
