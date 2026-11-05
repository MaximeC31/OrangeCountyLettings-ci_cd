"""Views listing lettings and showing a single letting."""

import logging

from django.contrib import admin
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_http_methods
from .models import Letting

logger = logging.getLogger(__name__)


@admin.site.admin_view
@require_http_methods(["GET", "POST"])
def sentry_test(request):
    if request.method == "POST":
        raise RuntimeError("Synthetic Sentry test error")
    return render(request, "lettings/sentry_test.html")


def index(request):
    """Render the list of every letting."""
    lettings_list = Letting.objects.all()
    context = {"lettings_list": lettings_list}
    return render(request, "lettings/index.html", context)


def letting(request, letting_id):
    """Render one letting, or a 404 page when it does not exist."""
    logger.info("Letting detail requested.")
    letting = get_object_or_404(
        Letting.objects.select_related("address"), id=letting_id
    )
    context = {
        "title": letting.title,
        "address": letting.address,
    }
    return render(request, "lettings/letting.html", context)
