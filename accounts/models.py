from django.db import models
from django.contrib.auth.models import User



class Skill(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Навык'
    )

    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    name = models.CharField(
        max_length=100,
        verbose_name='Имя'
    )

    photo = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True
    )

    telegram = models.CharField(
        max_length=100,
        blank=True
    )

    skills = models.ManyToManyField(
        Skill,
        related_name='profiles',
        blank=True
    )

    def __str__(self):
        return self.name

