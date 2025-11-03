from django.core.management.base import BaseCommand
from users.models import CustomUser


class Command(BaseCommand):
    help = 'Add test courses to the database'

    def handle(self, *args, **kwargs):
        users = [
            {
                'email': 'user_one1@example.com', 'password': 'user_one1',
                'phone_number':'123456789', 'country': 'Russia'
            },
            {
                'email': 'user_two2@example.com', 'password': 'user_two2',
                'phone_number': '987654321', 'country': 'USA'
            },
            {
                'email': 'user_three3@example.com', 'password': 'user_three3',
                'phone_number': '321654987', 'country': 'Canada'
            }
        ]

        for user_data in users:
            user, created = CustomUser.objects.get_or_create(**user_data)
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully added user: {user.email}'))
            else:
                self.stdout.write(
                    self.style.WARNING(f'User already exists: {user.email}'))
