from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PatientViewSet,
    DossierMedicalViewSet,
    DocumentMedicalViewSet,
    PatientRegisterView,
    MyPatientProfileView,
    MyDossierMedicalView,
)

router = DefaultRouter()
router.register(r"patients", PatientViewSet, basename="patients")
router.register(r"dossier-medical", DossierMedicalViewSet, basename="dossier-medical")
router.register(r"documents", DocumentMedicalViewSet, basename="documents")

urlpatterns = [
    path("patients/register/", PatientRegisterView.as_view(), name="patient-register"),
    path("patients/me/", MyPatientProfileView.as_view(), name="my-profile"),
    path("patients/my-dossier/", MyDossierMedicalView.as_view(), name="my-dossier"),
    path("", include(router.urls)),
]

