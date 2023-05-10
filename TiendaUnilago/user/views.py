from rest_framework import generics, permissions, viewsets
from .serializers import UserSerializer
from core.models import User


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    #permission_classes = (permissions.IsAuthenticated,)

    # def create(self, request, *args, **kwargs):
    #     password = request.data.pop('password')


