from django.contrib import admin
from django.urls import path, include, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework import routers

from profiles import views as profile_views


schema_view = get_schema_view(
    openapi.Info(
        title="Documentation API",
        default_version="v1",
        description="Public API documentation",
        contact=openapi.Contact(email="agusticonesagago@gmail.com"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

routers = routers.DefaultRouter()

auth_patterns = (
    [
        path("login", profile_views.LoginApiView.as_view(), name="auth_login"),
        path("signup", profile_views.SignUpApiView.as_view(), name="auth_signup"),
        path("profiles", profile_views.ProfilesView.as_view(), name="auth_profiles"),
    ],
    "auth",
)

urlpatterns = [
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    re_path(
        r"^swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    re_path(
        r"^redoc/$", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
    ),
    path("login/", admin.site.login),
    path("admin/", admin.site.urls),
    path("api/", include(routers.urls)),
    path("api/token/", include(auth_patterns)),
]
