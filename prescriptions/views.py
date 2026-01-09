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

    def get_queryset(self):
        """Filter prescriptions based on user role"""
        from patients.models import Patient
        user = self.request.user
        queryset = Prescription.objects.all()
        
        if user.role == 'patient':
            # Patients see only their own prescriptions
            try:
                patient = Patient.objects.get(nom=user.username)
                queryset = queryset.filter(patient=patient)
            except Patient.DoesNotExist:
                return Prescription.objects.none()
        elif user.role == 'medecin':
            # Doctors see prescriptions where they are the assigned doctor
            queryset = queryset.filter(doctor=user)
        elif user.role == 'secretaire':
            # Secretaries see all prescriptions
            pass
        else:
            return Prescription.objects.none()
        
        return queryset


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


class MedicationList(generics.ListCreateAPIView):
    queryset = Medication.objects.filter(is_active=True)
    serializer_class = None
    permission_classes = [IsAuthenticated, IsMedecin]

    def get(self, request, *args, **kwargs):
        from django.http import JsonResponse
        medications = self.queryset.values('id', 'name', 'form', 'standard_dosage', 'description')
        return JsonResponse(list(medications), safe=False)

    def post(self, request, *args, **kwargs):
        from django.http import JsonResponse
        name = request.data.get('name')
        form = request.data.get('form', 'autre')
        standard_dosage = request.data.get('standard_dosage', '')
        description = request.data.get('description', '')
        
        if not name:
            return JsonResponse({'error': 'Name is required'}, status=400)
        
        medication = Medication.objects.create(
            name=name,
            form=form,
            standard_dosage=standard_dosage,
            description=description,
            is_active=True
        )
        
        return JsonResponse({
            'id': medication.id,
            'name': medication.name,
            'form': medication.form,
            'standard_dosage': medication.standard_dosage,
            'description': medication.description
        }, status=201)


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
