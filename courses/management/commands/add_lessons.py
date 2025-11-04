from django.core.management.base import BaseCommand
from courses.models import Lesson, Course
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = 'Add test courses to the database'

    def handle(self, *args, **kwargs):
        python_lessons = [
            {
                'name': 'Установка Python и настройка окружения',
                'description': 'Узнайте как установить Python на вашу операционную систему, настроить виртуальное окружение и выбрать IDE для комфортной работы. Первые шаги в мире Python.',
                'course': '2'
            },
            {
                'name': 'Переменные и типы данных в Python',
                'description': 'Изучите основные типы данных: числа, строки, списки, словари. Научитесь работать с переменными, преобразовывать типы и выполнять базовые операции.',
                'course': '2'
            },
            {
                'name': 'Условные операторы и циклы',
                'description': 'Освойте управление потоком выполнения программы. Условные конструкции if-elif-else, циклы for и while. Практические примеры использования.',
                'course': '2'
            },
            {
                'name': 'Функции и модули в Python',
                'description': 'Научитесь создавать собственные функции, работать с аргументами и возвращаемыми значениями. Импорт стандартных модулей и создание своих.',
                'course': '2'
            }
        ]
        django_lessons = [
            {
                'name': 'Введение в Django и создание первого проекта',
                'description': 'Знакомство с фреймворком Django, его архитектурой MVT. Установка Django, создание проекта и приложения. Структура Django проекта.',
                'course': '3'
            },
            {
                'name': 'Модели Django и работа с базой данных',
                'description': 'Создание моделей данных, использование ORM Django. Миграции базы данных. Связи между моделями: ForeignKey, ManyToMany, OneToOne.',
                'course': '3'
            },
            {
                'name': 'Представления (Views) и URL-маршрутизация',
                'description': 'Создание представлений на основе функций и классов. Настройка URL-маршрутов. Передача данных между представлениями и шаблонами.',
                'course': '3'
            },
            {
                'name': 'Шаблоны Django и статические файлы',
                'description': 'Работа с системой шаблонов Django. Теги шаблонов, фильтры, наследование. Подключение CSS, JavaScript и изображений.',
                'course': '3'
            }
        ]
        data_analysis_lessons = [
            {
                'name': 'Введение в анализ данных и установка библиотек',
                'description': 'Обзор процесса анализа данных. Установка и настройка Pandas, NumPy, Matplotlib. Знакомство с Jupyter Notebook для интерактивного анализа.',
                'course': '4'
            },
            {
                'name': 'Работа с Pandas: DataFrame и Series',
                'description': 'Создание и манипуляция DataFrame. Индексация, фильтрация, сортировка данных. Работа с пропущенными значениями и аномалиями.',
                'course': '4'
            },
            {
                'name': 'Анализ данных с помощью Pandas',
                'description': 'Группировка данных, агрегатные функции, сводные таблицы. Объединение и соединение DataFrame. Временные ряды и работа с датами.',
                'course': '4'
            },
            {
                'name': 'Визуализация данных с Matplotlib и Seaborn',
                'description': 'Создание графиков и диаграмм: линейные, столбчатые, круговые, scatter plot. Настройка стилей и оформления визуализаций.',
                'course': '4'
            }
        ]

        all_lessons = python_lessons + django_lessons + data_analysis_lessons
        for lesson_data in all_lessons:
            course = Course.objects.get(id=lesson_data['course'])
            lesson, created = Lesson.objects.get_or_create(
                name=lesson_data['name'],
                description=lesson_data['description'],
                course=course
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully added lesson: {lesson.name}'))
            else:
                self.stdout.write(
                    self.style.WARNING(f'Lesson already exists: {lesson.name}'))
