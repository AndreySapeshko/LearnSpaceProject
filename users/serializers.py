from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'avatar', 'phone_number', 'country', 'is_active', 'groups', 'last_login']

    def create(self, validated_data):
        """Создает пользователя с правильно хешированным паролем"""

        password = validated_data.pop('password')

        user = User(
            email=validated_data['email'],
            avatar=validated_data.get('avatar'),
            phone_number=validated_data.get('phone_number'),
            country=validated_data.get('country'),
            is_active=validated_data.get('is_active', True)
        )
        user.set_password(password)
        user.save()
        return user
