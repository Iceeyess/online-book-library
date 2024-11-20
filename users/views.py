from django.shortcuts import render
from rest_framework import viewsets, generics
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework_simplejwt.views import TokenObtainPairView

from users.models import User
from users.permissions import IsOwner, IsSuperuser
from users.serializers import UserSerializer, MyTokenObtainPairSerializer


# Create your views here.
class UsersViewSet(viewsets.ModelViewSet):
    """Class for user CRUD"""
    queryset = User.objects.all()
    serializer_class = UserSerializer


    def get_permissions(self):
        """Depends which action method returns list of permission classes"""
        if self.action == 'create':
            permission_classes = [AllowAny, ]
        elif self.action in ('retrieve', 'update', 'destroy', 'partial_update'):
            permission_classes = [IsSuperuser | IsAdminUser | IsOwner]
        elif self.action == 'list':
            permission_classes = [IsSuperuser | IsAdminUser ]
        return [permission() for permission in permission_classes]

class MyTokenObtainPairView(TokenObtainPairView):
    """Obtain token"""
    serializer_class = MyTokenObtainPairSerializer