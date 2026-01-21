from random import random
import uuid
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from .models import Profile, Skill, Like
import json
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
import secrets




@login_required
def magic(request):
    me = request.user.profile

    # Навыки текущего пользователя
    my_skills = set(me.skills.values_list('id', flat=True))

    # Профили, которые имеют хотя бы один навык, которого нет у меня
    candidates = Profile.objects.exclude(id=me.id).filter(
        skills__id__in=Skill.objects.exclude(id__in=my_skills)
    ).distinct()

    # Если есть кандидаты — выбираем случайного
    selected_profile = random.choice(candidates) if candidates else None

    return render(request, 'magic.html', {
        'profile': selected_profile
    })




@require_POST
@login_required
def toggle_like(request):
    profile_id = request.POST.get("profile_id")

    if not profile_id:
        return JsonResponse({"error": "No profile id"}, status=400)

    profile = get_object_or_404(Profile, id=profile_id)

    like, created = Like.objects.get_or_create(
        from_user=request.user,
        to_profile=profile
    )

    if not created:
        like.delete()
        liked = False
    else:
        liked = True

    return JsonResponse({
        "liked": liked,
    })





@login_required
def likes_list(request):
    likes = Like.objects.filter(from_user=request.user)
    return render(request, 'likes.html', {'likes': likes})





def skills_list(request):
    q = request.GET.get("q", "")
    skills = Skill.objects.filter(name__icontains=q)[:10]
    return JsonResponse(
        [{"id": s.id, "name": s.name} for s in skills],
        safe=False
    )




@login_required
def like_profile(request, profile_id):
    if request.method != 'POST':
        return redirect('/')

    profile = get_object_or_404(Profile, id=profile_id)

    if profile.user == request.user:
        return redirect(request.META.get('HTTP_REFERER', '/'))

    like = Like.objects.filter(
        from_user=request.user,
        to_profile=profile
    )

    if like.exists():
        like.delete()
    else:
        Like.objects.create(
            from_user=request.user,
            to_profile=profile
        )

    return redirect(request.META.get('HTTP_REFERER', '/'))



def profile_detail(request, slug):
    profile = get_object_or_404(Profile, slug=slug)
    return render(request, 'profile_detail.html', {
        'profile': profile
    })


def reg(request):
    if request.method == 'POST':
        profile = Profile.objects.create(
            name=request.POST['name'],
            telegram=request.POST['telegram'],
            photo=request.FILES.get('photo')
        )

        skills_ids = request.POST.getlist('skills')
        profile.skills.set(Skill.objects.filter(id__in=skills_ids))

        return JsonResponse({'success': True})


    skills = Skill.objects.all()
    return render(request, 'registration.html', {'skills': skills})





@require_POST

def register_profile(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=400)

    name = request.POST.get("name")
    telegram = request.POST.get("telegram")
    skills_raw = request.POST.get("skills")
    photo = request.FILES.get("photo")

    if not name or not telegram:
        return JsonResponse({"error": "Не все поля заполнены"}, status=400)

    # Разбираем навыки
    skills_ids = json.loads(skills_raw) if skills_raw else []

    # Генерируем уникальное имя пользователя
    username = f"user_{User.objects.count() + 1}"
    temp_password = secrets.token_urlsafe(8)  # случайный безопасный пароль

    # Создаём пользователя
    user = User.objects.create_user(
        username=username,
        password=temp_password
    )

    # Создаём профиль
    profile = Profile.objects.create(
        user=user,
        name=name,
        telegram=telegram,
        photo=photo
    )

    # Привязываем навыки, если есть
    if skills_ids:
        profile.skills.set(
            Skill.objects.filter(id__in=skills_ids)
        )

    # Автоматический вход пользователя
    login(request, user)

    # Возвращаем успешный JSON
    return JsonResponse({"success": True, "username": username})




@require_POST
def login_view(request):
    username = request.POST.get("username")
    password = request.POST.get("password")

    user = authenticate(request, username=username, password=password)

    if user is None:
        return JsonResponse(
            {"success": False, "error": "Неверный логин или пароль"},
            status=400
        )

    login(request, user)
    return JsonResponse({"success": True})

from django.shortcuts import render, get_object_or_404
from .models import Profile

def profile_detail(request, slug):
    profile = get_object_or_404(Profile, slug=slug)

    return render(request, 'profile_detail.html', {
        'profile': profile
    })
