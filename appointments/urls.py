from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import RendezVousViewSet

router = DefaultRouter()
router.register(r'rendez-vous', RendezVousViewSet, basename='rendez-vous')

urlpatterns = [
    # Explicit patterns for trailing slash compatibility
    path('rendez-vous/', RendezVousViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='rendezvous-list'),
    path('rendez-vous', RendezVousViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='rendezvous-list-no-slash'),
    path('rendez-vous/<int:pk>/', RendezVousViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='rendezvous-detail'),
    path('rendez-vous/<int:pk>', RendezVousViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='rendezvous-detail-no-slash'),
    # Custom action endpoints
    path('rendez-vous/by_doctor_date/', RendezVousViewSet.as_view({'get': 'by_doctor_date'}), name='rendezvous-by-doctor-date'),
    path('rendez-vous/by_doctor_date', RendezVousViewSet.as_view({'get': 'by_doctor_date'}), name='rendezvous-by-doctor-date-no-slash'),
    path('rendez-vous/by_creator/', RendezVousViewSet.as_view({'get': 'by_creator'}), name='rendezvous-by-creator'),
    path('rendez-vous/by_creator', RendezVousViewSet.as_view({'get': 'by_creator'}), name='rendezvous-by-creator-no-slash'),
]
