from django.urls import path

from . import views

app_name = "lettings"

urlpatterns = [
    path("", views.index, name="index"),
    path("sentry-test/", views.sentry_test, name="sentry_test"),
    path("<int:letting_id>/", views.letting, name="letting"),
]
