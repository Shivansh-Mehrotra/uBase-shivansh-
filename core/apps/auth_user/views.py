import json
from datetime import datetime
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions
from rest_framework import status as http_status_codes
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken

from core.apps.permission.models import ModuleAction
from core.apps.auth_user.helpers import send_reset_password_mailer
from core.apps.role.models import AppSource
from core.auth.serializers import ChangePasswordSerializer, LoginSerializer, ForgotPasswordSerializer, \
    ResetPasswordSerializer, ValidateTokenSerializer

from core.tokens import make_token, check_token, get_token_data
from core.exceptions import BadRequestError, InvalidData
from core.response import SimpleMessageResponse, SimpleDataResponse

User = get_user_model()


class AuthUserViewSets(ViewSet):

    def _get_app_source(self, app_source):
        try:
            return AppSource.objects.get(source_key=app_source)
        except:
            raise BadRequestError("App-Source is required in HTTP request header")

    def get_permissions(self):
        if self.action == 'change_password':
            self.permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in self.permission_classes]

    def login(self, request):
        app_source = request.headers.get('app-source')
        app_source = self._get_app_source(app_source)

        login_serializer = LoginSerializer(data=request.data, context={
            'request': request,
            'app_source': app_source
        })
        try:
            login_serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        user = login_serializer.user
        if user.is_active:
            user.last_login = timezone.now()
            user.save()
            request.user = user
            # access_lof_info(request, params="logged in")
            return Response({'message': 'log-In Successful.', 'data': login_serializer.validated_data})
        return SimpleMessageResponse("User is not Active in system", http_status_codes.HTTP_423_LOCKED)

    def logout(self, request):
        # TODO: get best us of authentication by using Oauth 2 to invalidate token.
        user = request.user
        if user.is_authenticated:
            pass
        return SimpleMessageResponse("Successfully logged out.")

    def change_password(self, request):
        params = request.data
        serializers = ChangePasswordSerializer(data=params)
        serializers.is_valid(raise_exception=True)

        if not request.user.check_password(params['old_password']):
            raise BadRequestError("Current Password does not match")

        request.user.set_password(params['new_password'])
        request.user.save()

        return SimpleMessageResponse('Password is successfully updated')

    def forget_password(self, request):
        params = request.data
        serializers = ForgotPasswordSerializer(data=params)
        serializers.is_valid(raise_exception=True)

        try:
            user = User.objects.get(email=params['email'])
        except ObjectDoesNotExist:
            raise BadRequestError(f"No User found with email id {params['email']}.")

        if send_reset_password_mailer(user):
            return SimpleMessageResponse("Password reset link sent on your registered email id.")

        return Response({
            "message": '',
        }, status=http_status_codes.HTTP_400_BAD_REQUEST)

    def validate_token(self, request):
        params = request.data
        serializers = ValidateTokenSerializer(data=params)
        data = serializers.is_valid(raise_exception=True)
        return Response({
            "message": "Successfully verified.",
            "data": {
                "is_reset_token_expire": False
            }
        })

    def reset_password(self, request):
        params = request.data
        serializers = ResetPasswordSerializer(data=params)
        serializers.is_valid(raise_exception=True)
        data = serializers.data
        token_data = data.get('reset_token', {})

        try:
            user = User.objects.get(email=token_data.get('email'))
        except ObjectDoesNotExist:
            raise BadRequestError(f"No User found with email id {data['email']}.")

        user.set_password(data['new_password'])
        user.save()
        return Response({
            "message": "Password has been set successfully. Please login to continue"
        })


class PermissionViewSet(ViewSet):
    permission_classes = (permissions.IsAuthenticated,)

    def user_permission(self, request):
        user = request.user
        data = {}
        module_actions_ids = set()

        app_source_id = request.query_params.get('app_source_id')
        app_source = request.query_params.get('app_source')
        module_key = request.query_params.get('module_key')

        params = {'is_active': True}
        if module_key:
            params['module__module_key'] = module_key

        if request.headers.get('app-source'):
            app_source = request.headers.get('app-source')

        if not request.user.is_superuser:
            # get all module action ids
            module_actions_ids.update(
                [
                    _ for _ in
                    user.roles.values_list('module_actions__id', flat=True) if _  # from role
                ] +
                [
                    _ for _ in
                    user.module_actions.values_list('id', flat=True) if _   # from user
                ]
            )

        # get data for module action
        if module_actions_ids:
            params['id__in'] = module_actions_ids

        if app_source_id:
            params['module__app_source_id'] = app_source_id

        if app_source:
            params['module__app_source__source_key'] = app_source

        # FIXME: if this query takes time for large data split it in parts
        module_actions = ModuleAction.objects.filter(**params).values(
            'id', 'action', 'label', 'order', 'description', 'route_url', 'is_routable',
            'module_id', 'module__module_key', 'module__label', 'module__order', 'module__description',
            'module__parent_id', 'module__parent__module_key', 'module__parent__label',
            'module__parent__order', 'module__parent__description',
            'module__parent__parent_id'
        )
        # TODO add feature for multi level tree structure
        for action in module_actions:
            # add module obj if not
            if action['module__module_key'] not in data:
                data[action['module__module_key']] = {
                    "id": action["module_id"],
                    "label": action["module__label"],
                    "order": action["module__order"],
                    "description": action["module__description"],
                    "parent_id": action["module__parent_id"],
                    "actions": {}
                }
            # add action in module key
            data[action['module__module_key']]['actions'].update({
                action["action"]: {
                    "id": action["id"],
                    "label": action["label"],
                    "order": action["order"],
                    "description": action["description"],
                    "route_url": action["route_url"],
                    "is_routable": action["is_routable"]
                }
            })
            # add parent module obj if not
            if action['module__parent__module_key'] not in data and action['module__parent_id']:
                data[action['module__parent__module_key']] = {
                    "id": action["module__parent_id"],
                    "label": action["module__parent__label"],
                    "order": action["module__parent__order"],
                    "description": action["module__parent__description"],
                    "parent_id": action["module__parent__parent_id"],
                    "actions": {}
                }

        return SimpleDataResponse(data)
