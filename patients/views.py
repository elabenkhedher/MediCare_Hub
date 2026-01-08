# patients/views.py
from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Patient, DossierMedical, DocumentMedical
from .serializers import PatientSerializer, DossierMedicalSerializer, DocumentMedicalSerializer, PatientRegisterSerializer
from .permissions import IsSecretaire, IsMedecin, IsPatient
from accounts.serializers import UserSerializer


class MedecinListView(generics.ListAPIView):
    """Endpoint pour lister les médecins disponibles"""
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        from accounts.models import User
        return User.objects.filter(role='medecin')


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Allow both secretaire and medecin to access patient list
        user = self.request.user
        if user.is_authenticated and user.role in ['secretaire', 'medecin']:
            return Patient.objects.all()
        return Patient.objects.none()

    def perform_create(self, serializer):
        patient = serializer.save()
        DossierMedical.objects.create(patient=patient)

    def create(self, request, *args, **kwargs):
        # Custom create to handle permission check
        if request.user.is_authenticated and request.user.role in ['secretaire', 'medecin']:
            return super().create(request, *args, **kwargs)
        return Response({"detail": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)


class DossierMedicalViewSet(viewsets.ModelViewSet):
    queryset = DossierMedical.objects.all()
    serializer_class = DossierMedicalSerializer
    permission_classes = [IsAuthenticated, IsSecretaire]


class DocumentMedicalViewSet(viewsets.ModelViewSet):
    queryset = DocumentMedical.objects.all()
    serializer_class = DocumentMedicalSerializer
    permission_classes = [IsAuthenticated, IsSecretaire]


class PatientRegisterView(generics.CreateAPIView):
    serializer_class = PatientRegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()
        refresh = RefreshToken.for_user(user)

        return Response({
            "message": "Inscription réussie",
            "user_id": user.id,
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }, status=status.HTTP_201_CREATED)


class MyPatientProfileView(generics.RetrieveUpdateAPIView):
    """Endpoint pour que le patient connecté puisse voir et modifier son propre profil"""
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated, IsPatient]

    def get_object(self):
        # Trouver le patient lié à l'utilisateur connecté
        patient = Patient.objects.filter(nom=self.request.user.username).first()
        if not patient:
            # Si pas trouvé par nom, créer un patient pour cet utilisateur
            patient = Patient.objects.create(
                nom=self.request.user.username,
                email=self.request.user.email or "",
            )
            DossierMedical.objects.create(patient=patient)
        return patient


class MyDossierMedicalView(generics.RetrieveUpdateAPIView):
    """Endpoint pour que le patient connecté puisse voir et modifier son dossier médical"""
    serializer_class = DossierMedicalSerializer
    permission_classes = [IsAuthenticated, IsPatient]

    def get_object(self):
        # Trouver le patient lié à l'utilisateur connecté
        patient = Patient.objects.filter(nom=self.request.user.username).first()
        if not patient:
            # Ne pas créer automatiquement - retourner 404
            from django.http import Http404
            raise Http404("Patient non trouvé")
        return patient.dossier

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class AddDocumentView(generics.CreateAPIView):
    """Endpoint pour que le patient connecté puisse ajouter un document à son dossier"""
    serializer_class = DocumentMedicalSerializer
    permission_classes = [IsAuthenticated, IsPatient]

    def perform_create(self, serializer):
        # Trouver le patient lié à l'utilisateur connecté
        patient = Patient.objects.filter(nom=self.request.user.username).first()
        if not patient:
            from django.http import Http404
            raise Http404("Patient non trouvé")
        dossier = patient.dossier
        serializer.save(dossier_medical=dossier)
