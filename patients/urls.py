# patients/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PatientViewSet, DossierMedicalViewSet

router = DefaultRouter()
router.register(r'patients', PatientViewSet, basename='patients')
router.register(r'dossier-medical', DossierMedicalViewSet, basename='dossier-medical')

urlpatterns = [
    path('', include(router.urls)),
]
