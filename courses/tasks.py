from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model

from courses.models import Course, Subscription

User = get_user_model()


@shared_task
def course_update_notice(course_id):
    course = Course.objects.filter(id=course_id).first()
    subscriptions = Subscription.objects.filter(course=course)
    from_email = settings.EMAIL_HOST_USER
    if subscriptions.exists:
        for subscription in subscriptions:
            user = subscription.user
            print(f'Hi, {user.email}! Course {course.name} updated!')
        # send_mail(
        #     subject=f'Обновление курса {course.name}',
        #     message=f'Сообщаем вам, что курс {course.name} который вы приобрели обновлен.',
        #     from_email=from_email,
        #     recipient_list=users_email
        # )
