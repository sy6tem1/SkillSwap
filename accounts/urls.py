from django.urls import path
from . import views
from .views import profile_detail, login_view, profile_edit

urlpatterns = [
    path('magic/', views.magic, name='magic'),
    path('magic/like/<int:profile_id>/', views.like_profile, name='like_profile'),
    path('magic/viewed/<int:profile_id>/', views.mark_viewed, name='mark_viewed'),
    path('profiles/<slug:slug>/', profile_detail, name='profile_detail'),
    path("api/skills/", views.skills_list, name="skills_list"),
    path("register/", views.register_profile, name="register"),
    path("login/", login_view, name="login"),
    path('likes/', views.likes_list, name='likes_list'),
    path('like/<int:profile_id>/', views.like_profile, name='like_profile'),
    path("likes/toggle/", views.toggle_like, name="toggle_like"),
    path('profile/', views.profile_edit, name='profile'),
    path('profile/edit', profile_edit, name='profile_edit'),
]



