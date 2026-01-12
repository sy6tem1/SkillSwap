from django.urls import path
from .views import profile_detail

urlpatterns = [
    path('profiles/<slug:slug>/', profile_detail, name='profile_detail'),
]
