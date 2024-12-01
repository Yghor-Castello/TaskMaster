from django.contrib import admin
from django.urls import path, include

from rest_framework import permissions
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

from drf_yasg import openapi
from drf_yasg.views import get_schema_view


schema_view = get_schema_view(
    openapi.Info(
        title="Task Master",
        default_version='v1',
        description="Task Master",
        contact=openapi.Contact(email="yghorcastello.backend@gmail.com"),
        license=openapi.License(name="Yghor Castello - Dev Backend Python"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('task_master.urls')),
    path('token/', TokenObtainPairView.as_view(), name='token'),
    path('token-refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    # Django Swagger
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'), 
]