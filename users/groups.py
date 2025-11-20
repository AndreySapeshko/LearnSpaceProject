from django.contrib.auth.models import Group, Permission


def create_or_update_group(group_name: str, permission_codenames: list) -> None:
    """ Создает группу пользователей и добавляет ей разрешения,
    если такая группа есть то добавляет ей разрешения если их там нет """

    group, created = Group.objects.get_or_create(name=group_name)
    if created:
        for codename in permission_codenames:
            perm = Permission.objects.get(codename=codename)
            group.permissions.add(perm)
            print(f'In new grop {group_name} successfully added permission: {codename}')
    else:
        for codename in permission_codenames:
            if not group.permissions.filter(codename=codename).exists():
                perm = Permission.objects.get(codename=codename)
                group.permissions.add(perm)
                print(f'In grop {group_name} successfully added permission: {codename}')
