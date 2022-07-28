"""school_management_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path, include,re_path
from school_management_system import settings
from django.conf.urls.static import static
from school import views
from bankapi import verify_student
from django.contrib.auth.decorators import login_required

from rest_framework import permissions
from drf_yasg.views import get_schema_view
# from rest_framework.schemas import get_schema_view
from drf_yasg import openapi
from django.views.generic import TemplateView

schema_view = get_schema_view(
    openapi.Info(
        title="MSAC API",
        default_version='v1',
        description="Welcome Mulan",
        terms_of_service="http://www.msac.edu.gh/about/",
        contact=openapi.Contact(email="terkpeh1990@gmail.com"),
        license=openapi.License(name="#"),
    ),
    public=False,
    permission_classes=(permissions.IsAuthenticated,),
)




urlpatterns = [
    # path('openapi', get_schema_view(
    #         title="Your Project",
    #         description="API for all things …",
    #         version="1.0.0"
    #     ), name='openapi-schema'),
    # path('swagger-ui/', TemplateView.as_view(
    #     template_name='swagger-ui.html',
    #     extra_context={'schema_url':'openapi-schema'}
    # ), name='swagger-ui'),
    re_path(r'^doc(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('doc/', schema_view.with_ui('swagger', cache_timeout=0),name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0),name='schema-redoc'),

    path('accounts/logout/', views.logout_request, name='django_registration_register'),


    path('docs',schema_view.as_view()),
    path('', views.login_view, name='log'),
    path('logouts', views.logout_request,name='logouts'),
    path('school/', include('school.urls', namespace='school')),
    path('shop/', include('bakery.urls', namespace='shop')),
    path('partytree/', include('partytree.urls', namespace='partytree')),
    path('salon/', include('salon.urls', namespace='salon')),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('admin/', admin.site.urls),

    #bank Api
    path('students',verify_student.student.as_view()),
    path('payment',verify_student.payment.as_view()),
]

urlpatterns += static(settings.MEDIA_URL,
                      document_root=settings.MEDIA_ROOT)
