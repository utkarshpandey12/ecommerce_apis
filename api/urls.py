from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import OrderViewSet, ProductViewSet

router = DefaultRouter()
router.trailing_slash = "/?"
router.register(r"products", ProductViewSet, basename="product")
router.register(r"orders", OrderViewSet, basename="order")

# URL Configuration
urlpatterns = [
    path("", include(router.urls)),
]
