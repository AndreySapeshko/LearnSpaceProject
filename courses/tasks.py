import logging

from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model

from courses.models import Course, Subscription

User = get_user_model()

logger = logging.getLogger('courses')


@shared_task
def course_update_notice(course_id):
    logger.info('Start task "course_update_notice"')
    course = Course.objects.filter(id=course_id).first()
    emails = list(Subscription.objects.filter(course=course).values_list('user__email', flat=True))
    from_email = settings.EMAIL_HOST_USER
    if not emails:
        return
    # for email in emails:
    #     print(f'Hi, {email}! Course {course.name} updated!')
    send_mail(
        subject=f'Обновление курса {course.name}',
        message=f'Сообщаем вам, что курс {course.name} который вы приобрели обновлен.',
        from_email=from_email,
        recipient_list=emails
    )
