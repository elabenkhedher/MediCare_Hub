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
        """Filter appointments based on user role"""
        from patients.models import Patient
        user = self.request.user
        if user.role == 'patient':
            # Patients see only their own appointments
            # Find the patient by matching nom with username
            try:
                patient = Patient.objects.get(nom=user.username)
                return RendezVous.objects.filter(patient=patient)
            except Patient.DoesNotExist:
                return RendezVous.objects.none()
        elif user.role == 'medecin':
            # Doctors see appointments where they are the assigned doctor
            return RendezVous.objects.filter(medecin=user)
        elif user.role == 'secretaire':
            # Secretaries see all appointments
            return RendezVous.objects.all()
        return RendezVous.objects.none()

    def perform_create(self, serializer):
        """Save the appointment with the current user as creator"""
        user = self.request.user
        
        # If patient is creating, auto-assign their patient profile
        if user.role == 'patient':
            from patients.models import Patient
            try:
                patient = Patient.objects.get(nom=user.username)
                serializer.save(created_by=user, patient=patient)
            except Patient.DoesNotExist:
                # If no patient profile exists, just save with created_by
                serializer.save(created_by=user)
        else:
            serializer.save(created_by=user)

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
        medecin_id = request.query_params.get('medecin_id')
        date = request.query_params.get('date')
        
        if not medecin_id or not date:
            return Response({'error': 'medecin_id and date are required'}, status=400)
        
        appointments = RendezVous.objects.filter(
            medecin_id=medecin_id,
            date=date
        ).values('heure_debut', 'heure_fin')
        
        return Response(list(appointments))
