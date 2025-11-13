from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model

User = get_user_model()


@shared_task
def remove_inactive_users():
    """Деактивирует пользователей неактивных более 30 дней"""

    thirty_days_ago = timezone.now() - timedelta(days=30)

    inactive_users = User.objects.filter(
        is_active=True,
        last_login__lt=thirty_days_ago
    )

    count = inactive_users.count()
    inactive_users.update(is_active=False)

    print(f"Deactivated {count} inactive users")
    return f"Deactivated {count} users"