from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register('product', views.ProductViewSet)
router.register('manufacturer', views.ManufacturerViewSet)
router.register('product-type', views.ProductTypeViewSet)
router.register('role', views.RoleViewSet)
router.register('client', views.ClientViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('make-purchase', views.make_purchase, name='make purchase'),
]
