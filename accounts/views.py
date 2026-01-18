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
    name = request.POST.get("name", "").strip()
    telegram = request.POST.get("telegram", "").strip()
    skills_raw = request.POST.get("skills")
    photo = request.FILES.get("photo")

    if not name or not telegram:
        return JsonResponse({
            "success": False,
            "error": "Заполните все поля"
        }, status=400)

    # 🔐 уникальный username
    base_username = name.lower().replace(" ", "_")
    username = base_username
    counter = 1

    while User.objects.filter(username=username).exists():
        counter += 1
        username = f"{base_username}{counter}"

    user = User.objects.create_user(
        username=username,
        password=User.objects.make_random_password()
    )

    profile = Profile.objects.create(
        user=user,
        name=name,
        telegram=telegram,
        photo=photo
    )

    if skills_raw:
        try:
            skills_ids = json.loads(skills_raw)
            profile.skills.set(
                Skill.objects.filter(id__in=skills_ids)
            )
        except json.JSONDecodeError:
            pass

    login(request, user)

    return JsonResponse({"success": True})




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

