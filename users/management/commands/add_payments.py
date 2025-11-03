from django.core.management.base import BaseCommand
from courses.models import Course, Lesson
from users.models import Payments
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = 'Add test courses to the database'

    def handle(self, *args, **kwargs):
        course_payments = [
            {
                'user': '5',
                'payment_date': '2024-10-15',
                'course': '2',
                'amount': 7500,
                'payment_method': 'transfer'
            },
            {
                'user': '6',
                'payment_date': '2024-09-22',
                'course': '3',
                'amount': 8900,
                'payment_method': 'cash'
            },
            {
                'user': '7',
                'payment_date': '2024-11-05',
                'course': '4',
                'amount': 6300,
                'payment_method': 'transfer'
            },
            {
                'user': '5',
                'payment_date': '2024-08-30',
                'course': '3',
                'amount': 9200,
                'payment_method': 'transfer'
            }
        ]
        lesson_payments = [
            {
                'user': '6',
                'payment_date': '2024-10-10',
                'lesson': '5',
                'amount': 3200,
                'payment_method': 'cash'
            },
            {
                'user': '7',
                'payment_date': '2024-09-18',
                'lesson': '9',
                'amount': 2800,
                'payment_method': 'transfer'
            },
            {
                'user': '5',
                'payment_date': '2024-11-12',
                'lesson': '12',
                'amount': 3500,
                'payment_method': 'cash'
            }
        ]

        for payment_data in course_payments:
            user = User.objects.get(id=payment_data['user'])
            course = Course.objects.get(id=payment_data['course'])
            payment, created = Payments.objects.get_or_create(
                user=user,
                payment_date=payment_data['payment_date'],
                course=course,
                amount=payment_data['amount'],
                payment_method=payment_data['payment_method']
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully added payment: {payment.id}'))
            else:
                self.stdout.write(
                    self.style.WARNING(f'Payment already exists: {payment.id}'))

        for payment_data in lesson_payments:
            user = User.objects.get(id=payment_data['user'])
            lesson = Lesson.objects.get(id=payment_data['lesson'])
            payment, created = Payments.objects.get_or_create(
                user=user,
                payment_date=payment_data['payment_date'],
                lesson=lesson,
                amount=payment_data['amount'],
                payment_method=payment_data['payment_method']
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully added payment: {payment.id}'))
            else:
                self.stdout.write(
                    self.style.WARNING(f'Payment already exists: {payment.id}'))
