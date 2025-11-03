from django.core.management.base import BaseCommand
from courses.models import Course
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = 'Add test courses to the database'

    def handle(self, *args, **kwargs):
        courses_data = [
            {
                'name': 'Python для начинающих: от основ до первых проектов',
                'description': 'Освойте основы Python через практические примеры. Научитесь писать чистый код, работать с данными и создавать простые приложения. Идеально для старта в программировании.',
                'user': '2'
            },
            {
                'name': 'Веб-разработка на Django: создание полноценных сайтов',
                'description': 'Полный курс по фреймворку Django. Изучите модели, представления, формы, аутентификацию и развертывание. Создадите собственный блог и интернет-магазин в процессе обучения.',
                'user': '3'
            },
            {
                'name': 'Анализ данных на Python: Pandas, NumPy и визуализация',
                'description': 'Научитесь обрабатывать и анализировать данные с помощью Python. Освойте библиотеки Pandas, NumPy, Matplotlib и Seaborn. Работа с реальными датасетами и построение отчетов.',
                'user': '4'
            }
        ]

        for course_data in courses_data:
            user = User.objects.get(id=course_data['user'])
            course, created = Course.objects.get_or_create(
                name=course_data['name'],
                description=course_data['description'],
                user=user
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully added course: {course.name}'))
            else:
                self.stdout.write(
                    self.style.WARNING(f'Course already exists: {course.name}'))
