from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

from courses.models import Course


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