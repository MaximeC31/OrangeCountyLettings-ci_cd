"""Views listing profiles and showing a single profile."""

import logging

from django.shortcuts import get_object_or_404, render
from .models import Profile

logger = logging.getLogger(__name__)


def index(request):
    """Render the list of every profile."""
    profiles_list = Profile.objects.select_related("user")
    context = {'profiles_list': profiles_list}
    return render(request, 'profiles/index.html', context)


def profile(request, username):
    """Render one profile, or a 404 page when the username has no profile."""
    logger.info("Profile detail requested.")
    profile = get_object_or_404(
        Profile.objects.select_related("user"), user__username=username
    )
    context = {'profile': profile}
    return render(request, 'profiles/profile.html', context)
