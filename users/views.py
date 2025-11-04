from rest_framework.generics import CreateAPIView


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer
