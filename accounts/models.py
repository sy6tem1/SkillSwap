from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from unidecode import unidecode
from django.conf import settings



class Skill(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Навык',
    )

    def __str__(self):
        return self.name



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    description = models.TextField(
        max_length=700,
        blank=True,
        default='Описание ещё не добавлено'
    )


    name = models.CharField(
        max_length=100

    )


    photo = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True
    )


    telegram = models.CharField(
        max_length=100,
        blank=False
    )


    skills = models.ManyToManyField(
        Skill,
        related_name='profiles',
        blank=True

    )


    slug = models.SlugField(
        max_length=120,
        unique=True,
        blank=True
    )




    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(unidecode(self.name))

            if not base_slug:
                base_slug = "user"

            slug = base_slug
            counter = 1

            while Profile.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name




class Like(models.Model):
    from_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='given_likes'
    )
    to_profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='received_likes'
    )

    class Meta:
        unique_together = ('from_user', 'to_profile')


    def __str__(self):
        return f'{self.from_user} -> {self.to_profile}'

from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL

class ProfileView(models.Model):
    viewer = models.ForeignKey(User, related_name='views_made', on_delete=models.CASCADE)
    viewed = models.ForeignKey(User, related_name='views_received', on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('viewer', 'viewed')