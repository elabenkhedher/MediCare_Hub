from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import RendezVous
from .serializers import RendezVousSerializer
from patients.permissions import IsSecretaire, IsMedecin

class RendezVousViewSet(viewsets.ModelViewSet):
    queryset = RendezVous.objects.all()
    serializer_class = RendezVousSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
