from django.urls import path, include
from rest_framework.routers import DefaultRouter

from app.views import FabricanteViewSet, ComponenteViewSet, buscar_produtos_externos

router = DefaultRouter()
router.register(r"fabricantes", FabricanteViewSet, basename="fabricante")
router.register(r"componentes", ComponenteViewSet, basename="componente")

urlpatterns = [
    path("", include(router.urls)),
    path("produtos-externos/", buscar_produtos_externos, name="buscar-produtos-externos"),
]
