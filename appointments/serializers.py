from rest_framework import serializers
from .models import RendezVous
from accounts.models import User

MAX_RDV_PAR_JOUR = 20

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']

class RendezVousSerializer(serializers.ModelSerializer):
    medecin_name = serializers.SerializerMethodField()
    patient_name = serializers.SerializerMethodField()

    class Meta:
        model = RendezVous
        fields = '__all__'
        read_only_fields = ['statut', 'created_by', 'created_at', 'medecin_name']


    def get_medecin_name(self, obj):
        if obj.medecin:
            return f"Dr. {obj.medecin.first_name or ''} {obj.medecin.last_name or obj.medecin.username}"
        return "Médecin non spécifié"

    def get_patient_name(self, obj):
        if obj.patient:
            return f"{obj.patient.prenom or ''} {obj.patient.nom or ''}".strip()
        return "Patient non spécifié"

    def validate(self, data):
        # Use .get() to avoid KeyError for partial updates
        medecin = data.get('medecin')
        date = data.get('date')
        heure_debut = data.get('heure_debut')
        heure_fin = data.get('heure_fin')

        # Skip validation if any required field is missing
        if not all([medecin, date, heure_debut, heure_fin]):
            return data

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

        # Exclude current instance during updates
        if self.instance:
            conflits = conflits.exclude(id=self.instance.id)

        if conflits.exists():
            raise serializers.ValidationError(
                "Créneau horaire déjà occupé."
            )

        return data
