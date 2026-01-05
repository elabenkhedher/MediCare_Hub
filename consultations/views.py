from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Consultation
from .serializers import ConsultationSerializer
from patients.permissions import IsMedecin
from rest_framework.exceptions import PermissionDenied

class ConsultationViewSet(viewsets.ModelViewSet):
    serializer_class = ConsultationSerializer
    permission_classes = [IsAuthenticated, IsMedecin]

    def get_queryset(self):
        # Filtre sur les consultations non archivées
        user = self.request.user
        if user.role == 'medecin':
            # Le médecin ne voit que ses consultations
            return Consultation.objects.filter(is_archived=False, medecin=user)
        return Consultation.objects.none()

    def perform_destroy(self, instance):
        # Interdit la suppression → on archive
        if instance.is_archived:
            raise PermissionDenied("This consultation is already archived.")
        instance.is_archived = True
        instance.save()
