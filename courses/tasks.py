from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta, datetime
from django_celery_beat.models import PeriodicTask, \
    IntervalSchedule

from courses.models import Course

User = get_user_model()


@shared_task
def course_update_notice(course_id, users_email):
    course = Course.objects.filter(id=course_id).first()
    from_email = settings.EMAIL_HOST_USER
    if course:
        for user_email in users_email:
            print(f'Hi, {user_email}! Course {course.name} updated!')
        # send_mail(
        #     subject=f'Обновление курса {course.name}',
        #     message=f'Сообщаем вам, что курс {course.name} который вы приобрели обновлен.',
        #     from_email=from_email,
        #     recipient_list=users_email
        # )


@shared_task
def remove_inactive_users():
    users = User.objects.filter(is_active=True)
    thirty_days_ago = timezone.now() - timedelta(days=30)
    for user in users:
        if user.last_login and user.last_login < thirty_days_ago:
            user.is_active = False
            user.save()


schedule, created = IntervalSchedule.objects.get_or_create(
    every=1,
    period=IntervalSchedule.MINUTES,
)

task, created = PeriodicTask.objects.get_or_create(
    interval=schedule,
    name='Remove inactive',
    task='courses.tasks.remove_inactive_users'
)
