from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from accounts.models import Profile



def home(request):
    profiles = Profile.objects.all()
    return render(request, 'index.html', {'profiles': profiles})

def profile(request):
    return render(request, 'profile.html')

def magic(request):
    return render(request, 'magic.html')

@login_required
def likes(request):
    profiles = Profile.objects.filter(liked_by=request.user)
    return render(request, 'likes.html', {
        'profiles': profiles
    })

def reg(request):
    return render(request, 'registration.html')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('profile/', profile, name='profile'),
    path('magic/', magic, name='magic'),
    path('likes/', likes, name='likes'),
    path('reg/', reg, name='reg'),
    path('', include('accounts.urls')),
]

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)
