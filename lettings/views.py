"""Views listing lettings and showing a single letting."""

from django.shortcuts import get_object_or_404, render
from .models import Letting


def index(request):
    """Render the list of every letting."""
    lettings_list = Letting.objects.all()
    context = {'lettings_list': lettings_list}
    return render(request, 'lettings/index.html', context)


def letting(request, letting_id):
    """Render one letting, or a 404 page when it does not exist."""
    letting = get_object_or_404(Letting, id=letting_id)
    context = {
        'title': letting.title,
        'address': letting.address,
    }
    return render(request, 'lettings/letting.html', context)
