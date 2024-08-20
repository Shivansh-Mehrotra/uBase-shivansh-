from django.conf import settings
from django.core.signing import SignatureExpired
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password
from core.tokens import check_token, TokenSerializerField


class LoginSerializer(TokenObtainPairSerializer):
    """
    This serializer is user to collect token.

    When is_valid() function in called it calls validate() then get_token() in called.
    Any property set to the token object will be available in jwt token payload

    """
    default_error_messages = {
        'no_active_account': 'Invalid Credential or No active account found with the given email'
    }

    email = serializers.EmailField(required=False)

    # removed class method so that we can get prop from self
    def get_token(self, user):
        token = super().get_token(user)

        # Add custom payload
        token['email'] = user.email
        token['is_superuser'] = user.is_superuser
        token['is_staff'] = user.is_staff

        app_source = self.context['app_source']

        params = {}
        if app_source:
            params['app_source'] = app_source
        try:
            role = user.roles.get(**params)
            token['default_url'] = role.default_module_action.route_url
        except:
            token['default_url'] = settings.DEFAULT_FRONTEND_REDIRECT_URL

        return token


class ChangePasswordSerializer(serializers.Serializer):

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

    def validate(self, attrs):

        if len(attrs['new_password']) < 8 or len(attrs['new_password']) >= 45:
            raise serializers.ValidationError("New Password must be between 8 to 45 characters long")

        elif attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError("Password does not match")
        return attrs

    class Meta:
        fields = (
            'old_password', 'new_password', 'confirm_password',
        )


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)

    class Meta:
        fields = ('email',)


class ValidateTokenSerializer(serializers.Serializer):
    token = TokenSerializerField(required=True, return_data=True)


class ResetPasswordSerializer(serializers.Serializer):
    reset_token = TokenSerializerField(required=True, return_data=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

    def validate(self, attrs):
        validate_password(attrs['new_password'])
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError("Password does not match")
        return attrs

    class Meta:
        fields = (
            'reset_token', 'new_password', 'confirm_password',
        )
