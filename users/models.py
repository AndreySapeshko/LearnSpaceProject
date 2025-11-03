from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """ Класс описывающий модель пользователя """

    username = None
    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to='avatar/', blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    country = models.CharField(max_length=70, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Payments(models.Model):
    """ Класс описывающий модель платежи """

    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Наличные'),
        ('transfer', 'Перевод на счет')
    ]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='payments')
    payment_date = models.DateField(verbose_name='Дата оплаты')
    course = models.OneToOneField('courses.Course', on_delete=models.CASCADE)
    lesson = models.OneToOneField('courses.Lesson', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма оплаты')
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        default='transfer',
        verbose_name='Способ оплаты'
    )

