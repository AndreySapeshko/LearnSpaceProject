from django.core.management.base import BaseCommand
from courses.models import Course, Lesson
from users.groups import create_or_update_group


class Command(BaseCommand):
    help = 'Add test courses to the database'

    def handle(self, *args, **kwargs):
        codenames = [
            'view_course',
            'view_lesson',
            'change_course',
            'change_lesson'
        ]
        group_name = 'Moderators'

        create_or_update_group(group_name, codenames)

