"""Database model for user profiles."""

from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    """Extra information attached to a single user account."""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profiles_profile")
    favorite_city = models.CharField(max_length=64, blank=True)

    def __str__(self):
        """Return the username of the related user."""
        return self.user.username
