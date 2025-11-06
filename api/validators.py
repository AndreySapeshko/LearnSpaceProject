from rest_framework import serializers


class LinksTrustedSitesValidator:

    def __init__(self, field , trusted_sites: list):
        self.trusted_sites = trusted_sites
        self.field = field

    def __call__(self, value):
        link = dict(value).get(self.field)
        if link:
            is_trusted_site = False
            for trusted_site in self.trusted_sites:
                if link.startswith(trusted_site):
                    is_trusted_site = True
                    break

            if not is_trusted_site:
                raise serializers.ValidationError('На этот сайт ссылки запрещены.')
