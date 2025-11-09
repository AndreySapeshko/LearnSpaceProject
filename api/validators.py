from rest_framework import serializers


class LinksTrustedSitesValidator:
    """ Класс для проверки ссылок, что они ведут на разрешенные сайты """

    __fields__ = ('video_url',)

    def __init__(self, trusted_sites: list):
        self.trusted_sites = trusted_sites

    def __call__(self, attrs):
        for field_name in self.__fields__:
            link = attrs.get(field_name)
            if link:
                is_trusted_site = False
                for trusted_site in self.trusted_sites:
                    if link.startswith(trusted_site):
                        is_trusted_site = True
                        break

                if not is_trusted_site:
                    raise serializers.ValidationError('На этот сайт ссылки запрещены.')
        return attrs
