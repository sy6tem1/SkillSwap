from django.urls import path
from . import views
from .views import profile_detail, login_view

urlpatterns = [
    path('profiles/<slug:slug>/', profile_detail, name='profile_detail'),
    path("api/skills/", views.skills_list, name="skills_list"),
    path("register/", views.register_profile, name="register"),
    path("login/", login_view, name="login"),
    path("toggle-like/", views.toggle_like, name="toggle_like"),
]

