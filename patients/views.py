# patients/views.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Patient, DossierMedical
from .serializers import PatientSerializer, DossierMedicalSerializer
from .permissions import IsSecretaire, IsMedecin
from rest_framework_simplejwt.tokens import RefreshToken

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated, IsSecretaire]

    def perform_create(self, serializer):
        patient = serializer.save()
        DossierMedical.objects.create(patient=patient)

class DossierMedicalViewSet(viewsets.ModelViewSet):
    queryset = DossierMedical.objects.all()
    serializer_class = DossierMedicalSerializer