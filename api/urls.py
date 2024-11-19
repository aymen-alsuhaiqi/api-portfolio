from django.urls import path
from . import views
from .swagger import schema_view

urlpatterns = [
    path('v1/cr_user',views.cr_user),
    path('v1/cr_information',views.cr_infromation.as_view()),
    path('v1/login',views.login),
    path('v1/skills',views.SkillsView.as_view()),
    path('v1/experience',views.ExperienceView.as_view()),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
