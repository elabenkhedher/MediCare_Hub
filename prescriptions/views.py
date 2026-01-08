from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .models import Prescription, PrescriptionItem, Medication
from .serializers import PrescriptionSerializer
from patients.permissions import IsMedecin


class OrdonnanceListCreate(generics.ListCreateAPIView):
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer
    permission_classes = [IsAuthenticated]


class OrdonnanceDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer
    permission_classes = [IsAuthenticated]


class OrdonnancesByPatient(generics.ListAPIView):
    serializer_class = PrescriptionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        patient_id = self.kwargs['patient_id']
        return Prescription.objects.filter(patient_id=patient_id)


class MedicationList(generics.ListAPIView):
    queryset = Medication.objects.filter(is_active=True)
    serializer_class = None
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        from django.http import JsonResponse
        medications = self.queryset.values('id', 'name', 'form', 'standard_dosage', 'description')
        return JsonResponse(list(medications), safe=False)


class PrescriptionViewSet(viewsets.ModelViewSet):
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer
    permission_classes = [IsAuthenticated, IsMedecin]

    def perform_update(self, serializer):
        if self.get_object().is_finalized:
            raise PermissionDenied("Prescription is finalized and cannot be modified")
        serializer.save()
    
    def perform_destroy(self, instance):
        if instance.is_finalized:
            raise PermissionDenied("Prescription is finalized and cannot be deleted")
        instance.delete()
