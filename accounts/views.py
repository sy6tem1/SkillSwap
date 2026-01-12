from django.shortcuts import render
from accounts.models import Profile

def home(request):
    query = request.GET.get('q')

    profiles = Profile.objects.all()

    if query:
        profiles = profiles.filter(
            skills__name__icontains=query
        ).distinct()

    return render(request, 'index.html', {
        'profiles': profiles
    })
