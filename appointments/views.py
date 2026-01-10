from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import RendezVous
from .serializers import RendezVousSerializer


class RendezVousViewSet(viewsets.ModelViewSet):
    queryset = RendezVous.objects.all()
    serializer_class = RendezVousSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter appointments based on user role and date parameter"""
        from patients.models import Patient
        user = self.request.user
        queryset = RendezVous.objects.all()
        
        # Get date filter from query params
        date_param = self.request.query_params.get('date')
        
        if user.role == 'patient':
            # Patients see only their own appointments
            # Find the patient by user or by matching nom with username
            try:
                patient = Patient.objects.get(user=user)
            except Patient.DoesNotExist:
                try:
                    patient = Patient.objects.get(nom=user.username)
                except Patient.DoesNotExist:
                    return RendezVous.objects.none()
            queryset = queryset.filter(patient=patient)
        elif user.role == 'medecin':
            # Doctors see appointments where they are the assigned doctor
            queryset = queryset.filter(medecin=user)
        elif user.role == 'secretaire':
            # Secretaries see all appointments
            pass
        else:
            return RendezVous.objects.none()
        
        # Apply date filter if provided
        if date_param:
            queryset = queryset.filter(date=date_param)
        
        return queryset.order_by('date', 'heure_debut')

    def perform_create(self, serializer):
        """Save the appointment with the current user as creator"""
        from patients.models import Patient
        user = self.request.user
        
        # Check if patient_id is provided in the request data (for doctor/secretaire creating appointment)
        patient_id = self.request.data.get('patient')
        
        patient = None
        if patient_id:
            # Use the patient_id from request (for doctor/secretaire)
            try:
                patient = Patient.objects.get(id=patient_id)
            except Patient.DoesNotExist:
                pass
        
        # If patient is creating their own appointment, auto-assign their patient profile
        if user.role == 'patient' and not patient:
            try:
                # Try to find by user relationship first
                patient = Patient.objects.get(user=user)
            except Patient.DoesNotExist:
                try:
                    # Fallback to nom matching
                    patient = Patient.objects.get(nom=user.username)
                except Patient.DoesNotExist:
                    pass
        
        # If no patient found, raise an error
        if not patient:
            raise serializers.ValidationError({"patient": "Patient profile not found for the current user"})
        
        serializer.save(created_by=user, patient=patient)

    def create(self, request, *args, **kwargs):
        """Override create to handle validation errors properly"""
        try:
            return super().create(request, *args, **kwargs)
        except Exception as e:
            return Response(
                {'non_field_errors': [str(e)]},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=['get'])
    def by_doctor_date(self, request):
        """Get appointments for a specific doctor on a specific date"""
        medecin_id = request.query_params.get('medecin') or request.query_params.get('medecin_id')
        date = request.query_params.get('date')

        if not medecin_id or not date:
            return Response({'error': 'medecin and date are required'}, status=400)

        appointments = RendezVous.objects.filter(
            medecin_id=medecin_id,
            date=date
        ).values('heure_debut', 'heure_fin')

        return Response(list(appointments))

    @action(detail=False, methods=['get'])
    def by_creator(self, request):
        """Get appointments created by the current user"""
        user = request.user
        appointments = RendezVous.objects.filter(created_by=user)
        serializer = self.get_serializer(appointments, many=True)
        return Response(serializer.data)

