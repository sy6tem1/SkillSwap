from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from accounts.models import Profile




def home(request):
    query = request.GET.get('q')

    profiles = Profile.objects.prefetch_related('skills')

    if query:
        profiles = profiles.filter(
            skills__name__icontains=query
        ).distinct()

    liked_profile_ids = set()

    if request.user.is_authenticated:
        liked_profile_ids = set(
            Profile.objects.filter(
                received_likes__from_user=request.user
            ).values_list('id', flat=True)
        )

    print("USER:", request.user)
    print("LIKED IDS:", liked_profile_ids)

    return render(request, 'index.html', {
        'profiles': profiles,
        'liked_profile_ids': liked_profile_ids,
    })



def profile(request):
    return render(request, 'profile.html')

def magic(request):
    return render(request, 'magic.html')

@login_required
def likes(request):
    profiles = Profile.objects.filter(received_likes__from_user=request.user)
    return render(request, 'likes.html', {
        'profiles': profiles
    })

def reg(request):
    return render(request, 'registration.html')

@login_required
def profile_edit(request):
    profile = request.user.profile


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('profile/', profile, name='profile'),
    path('magic/', magic, name='magic'),
    path('likes/', likes, name='likes'),
    path('reg/', reg, name='reg'),
    path('', include('accounts.urls')),
    path("accounts/", include("accounts.urls")),
    path('profile/edit/', profile_edit, name='profile_edit')

]

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)

