from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PlacementViewSet, StudentViewSet, ApplicationViewSet, statistics_view

router = DefaultRouter()
router.register(r'placements', PlacementViewSet)
router.register(r'students', StudentViewSet)
router.register(r'applications', ApplicationViewSet)

urlpatterns = [
    path('statistics/', statistics_view, name='statistics_api'),
    path('', include(router.urls)), 
]
