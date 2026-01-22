
from functools import wraps
from django.shortcuts import redirect

def profile_required(view_func):
    """
    Декоратор, который проверяет, есть ли у пользователя профиль.
    Если нет — редирект на страницу регистрации.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('reg')  # пользователь не залогинен
        if not hasattr(request.user, 'profile'):
            return redirect('reg')  # нет профиля
        return view_func(request, *args, **kwargs)
    return _wrapped_view
