from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import UserRegisterSerializer
from .claim_serializers import CustomTokenObtainPairSerializer
from patients.models import Patient, DossierMedical


class CustomTokenObtainPairView(TokenObtainPairView):
    """Custom token view that includes role in the response"""
    serializer_class = CustomTokenObtainPairSerializer


class UserRegisterView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        # Créer un Patient automatiquement si le rôle est "patient"
        if user.role == 'patient':
            patient = Patient.objects.create(
                nom=user.username,  # Utiliser le username comme nom par défaut
                prenom="",
                email=user.email or "",
            )
            # Créer le dossier médical
            DossierMedical.objects.create(patient=patient)

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "message": "Inscription réussie",
                "user_id": user.id,
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            },
            status=status.HTTP_201_CREATED,
        )
