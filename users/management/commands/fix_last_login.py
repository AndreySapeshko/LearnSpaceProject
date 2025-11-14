from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = 'Update last_login for existing users'

    def handle(self, *args, **options):
        # users = User.objects.filter(last_login__isnull=True)
        users = User.objects.all()

        for user in users:
            # Устанавливаем last_login на дату создания аккаунта
            user.last_login = user.date_joined
            user.save()

        self.stdout.write(
            self.style.SUCCESS(
                f'Updated last_login for {users.count()} users'
            )
        )
