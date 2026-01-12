from django.core.management.base import BaseCommand
from accounts.models import Skill


SKILLS = [
    # Образование
    "Математика",
    "Подготовка к ЕГЭ по математике",
    "Физика",
    "Химия",
    "Биология",
    "Английский язык",
    "Немецкий язык",
    "Олимпиадная математика",

    # IT
    "Python",
    "Django",
    "HTML",
    "CSS",
    "JavaScript",
    "Git",
    "SQL",
    "Алгоритмы",
    "Unity",
    "Blender",
    "Figma",
    "UI/UX дизайн",

    # Хобби и спорт
    "Футбол",
    "Баскетбол",
    "Волейбол",
    "Шахматы",
    "Гитара",
    "Фортепиано",
    "Вокал",
    "Фотография",
    "Видеомонтаж",
    "Рисование",
    "3D моделирование",
]


class Command(BaseCommand):
    help = "Загрузить навыки в БД"

    def handle(self, *args, **kwargs):
        created_count = 0

        for skill_name in SKILLS:
            _, created = Skill.objects.get_or_create(name=skill_name)
            if created:
                created_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Навыки загружены. Добавлено: {created_count}"
            )
        )
