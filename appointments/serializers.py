from rest_framework import serializers
from .models import RendezVous

MAX_RDV_PAR_JOUR = 20

class RendezVousSerializer(serializers.ModelSerializer):

    class Meta:
        model = RendezVous
        fields = '__all__'
        read_only_fields = ['statut', 'created_by', 'created_at']

    def validate(self, data):
        medecin = data['medecin']
        date = data['date']
        heure_debut = data['heure_debut']
        heure_fin = data['heure_fin']

        # 1️⃣ Limite RDV / jour
        count = RendezVous.objects.filter(
            medecin=medecin,
            date=date
        ).count()

        if count >= MAX_RDV_PAR_JOUR:
            raise serializers.ValidationError(
                "Nombre maximum de rendez-vous atteint pour ce jour."
            )

        # 2️⃣ Chevauchement
        conflits = RendezVous.objects.filter(
            medecin=medecin,
            date=date,
            heure_debut__lt=heure_fin,
            heure_fin__gt=heure_debut
        )

        if conflits.exists():
            raise serializers.ValidationError(
                "Créneau horaire déjà occupé."
            )

        return data
