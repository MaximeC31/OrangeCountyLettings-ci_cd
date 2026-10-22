"""Home page view for the site root."""

from django.shortcuts import render


def index(request):
    """Render the home page."""
    return render(request, "index.html")
