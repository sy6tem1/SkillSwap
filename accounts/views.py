from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from .models import Profile, Skill
import json
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login




@login_required
def likes(request):
    profiles = request.user.profile.likes.all()
    return render(request, "likes.html", {"profiles": profiles})




def skills_list(request):
    q = request.GET.get("q", "")
    skills = Skill.objects.filter(name__icontains=q)[:10]
    return JsonResponse(
        [{"id": s.id, "name": s.name} for s in skills],
        safe=False
    )



@login_required
def toggle_like(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid method"}, status=405)

    profile_id = request.POST.get("profile_id")
    target = get_object_or_404(Profile, id=profile_id)
    me = request.user.profile

    if target in me.likes.all():
        me.likes.remove(target)
        liked = False
    else:
        me.likes.add(target)
        liked = True

    return JsonResponse({
        "liked": liked,
        "likes_count": target.liked_by.count()
    })




def home(request):
    query = request.GET.get('q')

    profiles = Profile.objects.all()

    if query:
        profiles = profiles.filter(
            skills__name__icontains=query
        ).distinct()

    return render(request, 'index.html', {
        'profiles': profiles
    })


def like_profile(request, profile_id):
    profile = get_object_or_404(Profile, id=profile_id)

    if request.user in profile.liked_by.all():
        profile.liked_by.remove(request.user)
    else:
        profile.liked_by.add(request.user)

    return redirect('home')


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





def register_profile(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=400)

    name = request.POST.get("name")
    telegram = request.POST.get("telegram")
    skills_raw = request.POST.get("skills")
    photo = request.FILES.get("photo")

    if not name or not telegram:
        return JsonResponse({"error": "Missing fields"}, status=400)

    skills_ids = json.loads(skills_raw) if skills_raw else []

    # создаём временного пользователя (без регистрации)
    user = User.objects.create(username=f"user_{User.objects.count() + 1}")

    profile = Profile.objects.create(
        user=user,
        name=name,
        telegram=telegram,
        photo=photo
    )

    if skills_ids:
        profile.skills.set(
            Skill.objects.filter(id__in=skills_ids)
        )

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

