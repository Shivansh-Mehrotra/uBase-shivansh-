from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import Permission
from rest_framework.exceptions import AuthenticationFailed

# TODO: BaseAuthenticationBackend for extending custom ModelBackend

class EmailAuthenticationBackend(ModelBackend):

    def authenticate(self, request=None, password=None, **kwargs):
        UserModel = get_user_model()
        params = {}
        try:
            if 'email' in kwargs:
                params['email'] = kwargs['email']

            if 'username' in kwargs:
                params['email'] = kwargs['username']

            user = UserModel.objects.get(**params)
            # TODO: handle app source while login
            # TODO: cache current app source in user obj and request obj
        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user


class CorePermissionBackend(ModelBackend):

    def get_role_permissions(self, user_obj, obj=None):
        """
         calling `_get_permissions` from super class to make sure permission set remain consistent
         throughout django
        """
        return self._get_permissions(user_obj, obj, 'role')

    def _get_role_permissions(self, user_obj):

        # TODO: add support for app source filter in roles
        #  roles = list(user_obj.roles.filter(app_source=get_current_app_source).values_list('id', flat=True))
        roles = list(user_obj.roles.values_list('id', flat=True))
        module_action_prem = Permission.objects.filter(moduleaction__role_module_action__role__in=roles)

        # get permission from roles
        role_prem = Permission.objects.filter(role__in=roles)

        return role_prem | module_action_prem

    def get_user_module_action_permissions(self, user_obj, obj=None):
        """
         calling `_get_permissions` from super class to make sure permission set remain consistent
         throughout django
        """
        return self._get_permissions(user_obj, obj, 'user_module_action')

    def _get_user_module_action_permissions(self, user_obj):
        return Permission.objects.filter(moduleaction__usermoduleaction__user=user_obj)

    def get_all_permissions(self, user_obj, obj=None):
        if not user_obj.is_active or user_obj.is_anonymous or obj is not None:
            return set()
        if not hasattr(user_obj, '_core_perm_cache'):
            user_obj._core_perm_cache = {
                *self.get_user_module_action_permissions(user_obj),
                *self.get_role_permissions(user_obj),
            }
        return user_obj._core_perm_cache


