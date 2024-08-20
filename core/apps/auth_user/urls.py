from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from .views import *
# from django.conf.urls import url

app_name = 'user'

urlpatterns = [
    path('token/refresh', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('user/permission', PermissionViewSet.as_view({'get': 'user_permission'})),

    path('login', AuthUserViewSets.as_view({'post': 'login'})),
    path('change_password', AuthUserViewSets.as_view({'post': 'change_password'})),
    path('forget_password', AuthUserViewSets.as_view({'post': 'forget_password'})),
    path('reset_password', AuthUserViewSets.as_view({'post': 'reset_password'})),
    path('validate_token', AuthUserViewSets.as_view({'post': 'validate_token'})),
    path('logout', AuthUserViewSets.as_view({'post': 'logout'}))
]
