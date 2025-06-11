# network/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NetworkNodeViewSet, ProductViewSet

router = DefaultRouter()
router.register(r"nodes", NetworkNodeViewSet)
router.register(r"products", ProductViewSet)

urlpatterns = [
    path("api/", include(router.urls)),
    path("api-auth/", include("rest_framework.urls")),
]  # network/urls.py

router = DefaultRouter()
router.register(r"nodes", NetworkNodeViewSet)
router.register(r"products", ProductViewSet)

urlpatterns = [
    path("api/", include(router.urls)),
    path("api-auth/", include("rest_framework.urls")),
]
