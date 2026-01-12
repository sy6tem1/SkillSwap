"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from accounts.models import Profile



def home(request):
    print("HOME FROM ACCOUNTS")  # или CORE — как назовёшь
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
]

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)
