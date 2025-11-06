from django.core.validators import URLValidator
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Course(models.Model):
    """ Класс описывающий модель Course (образовательный курс) """

    name = models.CharField(max_length=100, verbose_name='Название курса')
    description = models.CharField(max_length=300, verbose_name='Описание')
    preview = models.ImageField(
        upload_to='images/',
        blank=True,
        null=True,
        verbose_name='Иллюстрация'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='courses',
        verbose_name='Автор курса'
    )

    def __str__(self):
        return f'{self.name}: {self.description}'

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'
        ordering = ['name']


class Lesson(models.Model):
    """ Класс описывающий модель Lesson (уроки из курса) """

    name = models.CharField(max_length=100, verbose_name='Название урока')
    description = models.CharField(max_length=300, verbose_name='Описание')
    preview = models.ImageField(
        upload_to='images/',
        blank=True,
        null=True,
        verbose_name='Иллюстрация'
    )
    video_url = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        validators=[URLValidator()],
        verbose_name='Ссылка на видео',
        help_text='Ссылка на YouTube, Vimeo или другое видео'
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='lessons',
        verbose_name='Курс'
    )

    def __str__(self):
        return f'{self.name}: {self.description}'

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'
        ordering = ['name']
