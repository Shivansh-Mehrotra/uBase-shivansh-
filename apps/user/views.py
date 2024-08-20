from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model

from apps.user.serializers import UserBaseSerializer, UserCreateSerializer, UserUpdateSerializer, \
    UserProfileSerializer
from core.permissions import StrictDjangoModelPermissions
from core.viewsets import ModelViewSet

User = get_user_model()


class UsersViewSet(ModelViewSet):
    queryset = User.objects.filter(is_superuser=False)
    serializer_class = UserBaseSerializer
    search_fields = ('first_name', 'last_name', 'username', 'email',)

    ordering_fields_mapping = {}
    ordering_fields = ('first_name', 'last_name', 'username', 'email',)
    ordering = '-id'

    filterset_fields_mappings = {}
    filterset_fields = ['first_name', 'last_name', 'username', 'email']

    permission_classes = [IsAuthenticated, StrictDjangoModelPermissions]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            self.serializer_class = UserCreateSerializer
        elif self.request.method == 'PUT':
            self.serializer_class = UserUpdateSerializer
        return self.serializer_class


class UserProfileViewSet(ModelViewSet):
    queryset = User.objects.filter(is_deleted=False)
    serializer_class = UserProfileSerializer

    def get_object(self):
        return self.request.user

    permission_classes = [IsAuthenticated]


