from django.urls import path
from . import views
from .swagger import schema_view

urlpatterns = [
    path('api/v1/cr_user',views.cr_user),
    path('api/v1/cr_information',views.cr_infromation.as_view()),
    path('api/v1/login',views.login),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
