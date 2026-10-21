from django.urls import resolve

from . import views


def test_root_url_resolves_to_home_view():
    assert resolve("/").func is views.index


def test_admin_url_resolves_to_admin_namespace():
    assert resolve("/admin/").namespace == "admin"
