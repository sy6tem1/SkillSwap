from django.db import models
from django.contrib.auth.models import User


class Skill(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Навык',
    )

    def __str__(self):
        return self.name



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    description = models.TextField(max_length=700)

    name = models.CharField(max_length=100)

    photo = models.ImageField(upload_to='avatars/', blank=True, null=True)

    telegram = models.CharField(max_length=100, blank=False)

    skills = models.ManyToManyField(Skill, related_name='profiles', blank=True)

    liked_by = models.ManyToManyField(User, related_name='liked_profiles', blank=True)

    slug = models.SlugField(max_length=100, db_index=True, unique=True)

    def __str__(self):
        return self.name

