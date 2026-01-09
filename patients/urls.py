from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PatientViewSet,
    DossierMedicalViewSet,
    DocumentMedicalViewSet,
    PatientRegisterView,
    MyPatientProfileView,
    MyDossierMedicalView,
    AddDocumentView,
    MedecinListView,
)

router = DefaultRouter()
router.register(r"dossier-medical", DossierMedicalViewSet, basename="dossier-medical")
router.register(r"documents", DocumentMedicalViewSet, basename="documents")

urlpatterns = [
    # Explicit patient endpoints (no router to avoid trailing slash issues)
    path("patients/", PatientViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name="patient-list"),
    path("patients", PatientViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name="patient-list-no-slash"),
    path("patients/<int:pk>/", PatientViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name="patient-detail"),
    path("patients/<int:pk>", PatientViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name="patient-detail-no-slash"),
    path("patients/register/", PatientRegisterView.as_view(), name="patient-register"),
    path("patients/register", PatientRegisterView.as_view(), name="patient-register-no-slash"),
    path("patients/me/", MyPatientProfileView.as_view(), name="my-profile"),
    path("patients/me", MyPatientProfileView.as_view(), name="my-profile-no-slash"),
    path("patients/my-dossier/", MyDossierMedicalView.as_view(), name="my-dossier"),
    path("patients/my-dossier", MyDossierMedicalView.as_view(), name="my-dossier-no-slash"),
    path("patients/add-document/", AddDocumentView.as_view(), name="add-document"),
    path("patients/add-document", AddDocumentView.as_view(), name="add-document-no-slash"),
    path("patients/medecins/", MedecinListView.as_view(), name="medecins-list"),
    path("patients/medecins", MedecinListView.as_view(), name="medecins-list-no-slash"),
    path("", include(router.urls)),
]
