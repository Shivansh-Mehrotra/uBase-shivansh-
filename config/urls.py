"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include

from apps.sample.views import index

urlpatterns = [
    path("", index),
    path('admin/', admin.site.urls),
    path('admin_tools/', include('admin_tools.urls')),
    path("api/admin/", include("rest_framework.urls")),
    path('api/v1/', include('core.apps.auth_user.urls')),
    path('api/v1/', include('core.apps.role.urls')),
    path('api/v1/', include('apps.user.urls')),
    path('api/v1/sample/', include('apps.sample.urls')),
    path('api/v1/permission/', include('core.apps.permission.urls')),
    path('api/v1/lookup-management/', include('core.apps.lookup_management.urls')),
    path('api/v1/locality/', include('core.apps.locality.urls')),
    #shivansh
    path('api/v1/', include('apps.student.urls')),
]
