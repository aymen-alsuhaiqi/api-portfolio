from django.urls import path
from . import views
from .swagger import schema_view

urlpatterns = [
    path('api/v1/',views.cr_user),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
