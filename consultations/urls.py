from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import ConsultationViewSet

router = DefaultRouter()
router.register(r'consultations', ConsultationViewSet, basename='consultations')

urlpatterns = [
    # Explicit patterns for trailing slash compatibility
    path('consultations/', ConsultationViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='consultation-list'),
    path('consultations', ConsultationViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='consultation-list-no-slash'),
    path('consultations/<int:pk>/', ConsultationViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='consultation-detail'),
    path('consultations/<int:pk>', ConsultationViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='consultation-detail-no-slash'),
]
