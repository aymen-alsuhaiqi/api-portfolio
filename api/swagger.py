from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="dashboard API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://aymen-eng.duckdns.org",
        contact=openapi.Contact(email="engaymen.work@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)