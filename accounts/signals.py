import os
from django.conf import settings
from django.db.models.signals import pre_save, post_delete, post_save
from django.dispatch import receiver
from .models import Profile

AVATAR_DIR = os.path.join(settings.MEDIA_ROOT, 'avatars')


@receiver(pre_save, sender=Profile)
def delete_old_avatar(sender, instance, **kwargs):
    """Удаляет старый аватар, если загружен новый."""
    if not instance.pk:
        return  # новый профиль

    try:
        old_instance = Profile.objects.get(pk=instance.pk)
    except Profile.DoesNotExist:
        return

    if old_instance.photo and old_instance.photo != instance.photo:
        old_path = os.path.join(settings.MEDIA_ROOT, old_instance.photo.name)
        if os.path.isfile(old_path):
            os.remove(old_path)


@receiver(post_delete, sender=Profile)
def delete_avatar_on_delete(sender, instance, **kwargs):
    """Удаляет аватар при удалении профиля."""
    if instance.photo:
        path = os.path.join(settings.MEDIA_ROOT, instance.photo.name)
        if os.path.isfile(path):
            os.remove(path)


def cleanup_unused_avatars():
    """Удаляет все файлы в папке avatars, которые не используются профилями."""
    if not os.path.exists(AVATAR_DIR):
        return

    used_files = Profile.objects.exclude(photo='').values_list('photo', flat=True)
    used_files = [os.path.basename(f) for f in used_files]

    for filename in os.listdir(AVATAR_DIR):
        if filename not in used_files:
            file_path = os.path.join(AVATAR_DIR, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)


# --- автоматический вызов очистки при каждом сохранении или удалении ---
@receiver(post_save, sender=Profile)
def run_cleanup_after_save(sender, instance, **kwargs):
    cleanup_unused_avatars()


@receiver(post_delete, sender=Profile)
def run_cleanup_after_delete(sender, instance, **kwargs):
    cleanup_unused_avatars()
