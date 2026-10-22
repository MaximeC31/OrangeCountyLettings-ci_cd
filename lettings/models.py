"""Database models for rental addresses and lettings."""

from django.db import models
from django.core.validators import MaxValueValidator, MinLengthValidator


class Address(models.Model):
    """Postal address attached to a letting."""

    number = models.PositiveIntegerField(validators=[MaxValueValidator(9999)])
    street = models.CharField(max_length=64)
    city = models.CharField(max_length=64)
    state = models.CharField(max_length=2, validators=[MinLengthValidator(2)])
    zip_code = models.PositiveIntegerField(validators=[MaxValueValidator(99999)])
    country_iso_code = models.CharField(max_length=3, validators=[MinLengthValidator(3)])

    class Meta:
        """Admin display options for addresses."""

        verbose_name_plural = "addresses"

    def __str__(self):
        """Return the number followed by the street name."""
        return f'{self.number} {self.street}'


class Letting(models.Model):
    """Rental property described by a title and an address."""

    title = models.CharField(max_length=256)
    address = models.OneToOneField(Address, on_delete=models.CASCADE)

    def __str__(self):
        """Return the letting title."""
        return self.title
