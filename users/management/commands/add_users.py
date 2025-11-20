from django.core.management.base import BaseCommand
from users.models import CustomUser


class Command(BaseCommand):
    help = 'Add test courses to the database'

    def handle(self, *args, **kwargs):
        users = [
            {
                'email': 'user_four4@example.com', 'password': 'user_four4',
                'phone_number': '456123789', 'country': 'Russia'
            },
            {
                'email': 'user_five5@example.com', 'password': 'user_five5',
                'phone_number': '654987321', 'country': 'USA'
            },
            {
                'email': 'user_six6@example.com', 'password': 'user_six6',
                'phone_number': '987321654', 'country': 'Canada'
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
