from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .models import Prescription
from .serializers import PrescriptionSerializer
from patients.permissions import IsMedecin  # ton permission custom

class PrescriptionViewSet(viewsets.ModelViewSet):
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer
    permission_classes = [IsAuthenticated, IsMedecin]

    def perform_update(self, serializer):
        # Empêche la modification si l’ordonnance est finalisée
        if self.get_object().is_finalized:
            raise PermissionDenied("Prescription is finalized and cannot be modified")
        serializer.save()
    
    def perform_destroy(self, instance):
        # Empêche la suppression d'une ordonnance finalisée
        if instance.is_finalized:
            raise PermissionDenied("Prescription is finalized and cannot be deleted")
        instance.delete()
