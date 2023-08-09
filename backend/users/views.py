from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny

from users.models import User
from users.serializers import UserSerializer


class UserView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        return [IsAuthenticated()] if self.request.method == 'GET' else [AllowAny()]
