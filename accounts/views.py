from random import random
from django.contrib.auth.models import User
from .models import Profile, Skill, Like, ProfileView
import json
from django.contrib.auth import authenticate, login
from django.views.decorators.http import require_POST
import secrets
from .decorators import profile_required
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import random
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProfileForm
from django.views.decorators.csrf import csrf_exempt




@profile_required
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



User = get_user_model()


@login_required
def mark_viewed(request, profile_id):
    # Ищем профиль по id
    profile = get_object_or_404(Profile, id=profile_id)

    # Создаём запись просмотра, используя пользователя профиля
    ProfileView.objects.get_or_create(viewer=request.user, viewed=profile.user)

    return redirect('magic')




@profile_required
@login_required
@require_POST
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




@profile_required
def likes_list(request):
    # Получаем все Like, которые текущий юзер поставил другим профилям
    likes = Like.objects.filter(from_user=request.user).select_related('to_profile')

    # Извлекаем сами профили
    profiles = [like.to_profile for like in likes]

    return render(request, 'likes.html', {'profiles': profiles})





def skills_list(request):
    q = request.GET.get("q", "")
    skills = Skill.objects.filter(name__icontains=q)[:10]
    return JsonResponse(
        [{"id": s.id, "name": s.name} for s in skills],
        safe=False
    )



@login_required
@profile_required
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




@csrf_exempt
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




@profile_required
def profile_detail(request, slug):
    profile = get_object_or_404(Profile, slug=slug)

    return render(request, 'profile_detail.html', {
        'profile': profile
    })


@profile_required
@login_required
def profile(request):
    profile = request.user.profile
    print("PROFILE VIEW CALLED, METHOD =", request.method)

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)

        if form.is_valid():
            profile = form.save()

            skills_raw = request.POST.get("skills", "[]")
            skills_ids = json.loads(skills_raw)
            profile.skills.set(Skill.objects.filter(id__in=skills_ids))

            return redirect("profile")
        if not form.is_valid():
            print("FORM ERRORS:", form.errors)


    else:
        form = ProfileForm(instance=profile)

    return render(request, "profile.html", {
        "profile": profile,
        "form": form
    })


