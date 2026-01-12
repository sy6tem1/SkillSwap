from django.shortcuts import render, get_object_or_404, redirect
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


def like_profile(request, profile_id):
    profile = get_object_or_404(Profile, id=profile_id)

    if request.user in profile.liked_by.all():
        profile.liked_by.remove(request.user)
    else:
        profile.liked_by.add(request.user)

    return redirect('home')


def profile_detail(request, slug):
    profile = get_object_or_404(Profile, slug=slug)
    return render(request, 'profile_detail.html', {
        'profile': profile
    })