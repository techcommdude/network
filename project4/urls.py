"""project4 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import include, path
from rest_framework import routers
from django.contrib.auth import get_user_model
from network.views import PostViewSet, UserViewSet, FollowViewSet
# from quickstart import views
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
User = get_user_model()


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'api/users', UserViewSet, basename='users')
# TODO: http://127.0.0.1:8000/users/ will retrieve the users in the system.
# http://127.0.0.1:8000/users/?format=json
# http://127.0.0.1:8000/users/3/?format=json
# This opens the Django rest framework
# http://127.0.0.1:8000/users/?format=api
router.register(r'api/posts', PostViewSet, basename='posts')
# http://127.0.0.1:8000/api/posts/?format=json
# http://127.0.0.1:8000/api/posts/89/?format=json
# This opens the Django rest framework
# http://127.0.0.1:8000/api/posts/?format=api
router.register(r'api/follow', FollowViewSet, basename='follow')
# http://127.0.0.1:8000/api/follow/?format=json
# http://127.0.0.1:8000/api/follow/3/?format=json

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("network.urls")),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
     # OpenAPI 3 documentation with Swagger UI
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "swagger_api_docs/",
        SpectacularSwaggerView.as_view(
            template_name="swagger-ui.html", url_name="schema"
        ),
        name="swagger-ui",
    ),
]
