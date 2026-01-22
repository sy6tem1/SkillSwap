from random import random

from django.contrib.auth.models import User
from .models import Profile, Skill, Like
import json
from django.contrib.auth import authenticate, login

from django.views.decorators.http import require_POST

from django.contrib.auth import login
import secrets



import random
from django.contrib.auth.decorators import login_required

from .models import Profile, Skill, ProfileView


@login_required
def magic(request):
    me = request.user.profile

    my_skills = me.skills.values_list('id', flat=True)

    viewed_profiles = ProfileView.objects.filter(
        viewer=request.user
    ).values_list('viewed_id', flat=True)

    candidates = Profile.objects.exclude(
        id=me.id
    ).exclude(
        id__in=viewed_profiles
    ).filter(
        skills__id__in=Skill.objects.exclude(id__in=my_skills)
    ).distinct()

    selected_profile = random.choice(list(candidates)) if candidates.exists() else None

    return render(request, 'magic.html', {
        'profile': selected_profile
    })

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from .models import ProfileView  # твоя модель для просмотров

User = get_user_model()


@login_required
def mark_viewed(request, profile_id):
    # Получаем пользователя, которого просматриваем
    viewed_user = get_object_or_404(User, id=profile_id)

    # Создаём запись просмотра
    ProfileView.objects.get_or_create(viewer=request.user, viewed=viewed_user)

    return redirect('magic')
@login_required
def like_profile(request, profile_id):
    profile = get_object_or_404(Profile, id=profile_id)
    # Добавляем лайк (предполагаем ManyToManyField в Profile: likes = models.ManyToManyField(User, related_name='liked_by'))
    profile.likes.add(request.user)
    return redirect('magic')




from django.http import JsonResponse
@require_POST
@login_required
def toggle_like(request):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "not_authenticated"}, status=403)

    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=400)

    profile_id = request.POST.get("profile_id")
    if not profile_id:
        return JsonResponse({"error": "No profile id"}, status=400)

    profile = get_object_or_404(Profile, id=profile_id)

    # Проверка, чтобы нельзя было лайкать себя
    if hasattr(profile, 'user') and profile.user == request.user:
        return JsonResponse({"error": "Cannot like yourself"}, status=400)

    like, created = Like.objects.get_or_create(
        from_user=request.user,
        to_profile=profile
    )

    if not created:
        like.delete()
        liked = False
    else:
        liked = True

    return JsonResponse({"liked": liked})





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
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

@login_required
def profile(request):
    if hasattr(request.user, 'profile'):
        profile = request.user.profile
    else:
        profile = None
    return render(request, 'profile.html', {'profile': profile})

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def edit_profile(request):
    profile = request.user.profile  # если у тебя есть модель Profile
    if request.method == 'POST':
        # здесь логика обновления профиля
        pass
    return render(request, 'edit_profile.html', {'profile': profile})





@login_required
def profile_edit(request):
    profile = request.user.profile

    if request.method == "POST":
        name = request.POST.get("name", "")
        telegram = request.POST.get("telegram", "")
        skills_raw = request.POST.get("skills", "[]")

        try:
            skills_ids = json.loads(skills_raw)
        except json.JSONDecodeError:
            skills_ids = []

        profile.name = name
        profile.telegram = telegram
        profile.skills.set(
            Skill.objects.filter(id__in=skills_ids)
        )
        profile.save()

        return redirect("profile_edit")

    return render(request, "profile.html", {
        "profile": profile,
    })
