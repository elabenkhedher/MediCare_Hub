from rest_framework import serializers
from .models import Consultation
from patients.models import Patient

MAX_CONSULTATIONS_VISIBLES = 10


class ConsultationSerializer(serializers.ModelSerializer):

    patient = serializers.PrimaryKeyRelatedField(
        queryset=Patient.objects.all(),
        required=False,
        allow_null=True
    )
    
    medecin = serializers.PrimaryKeyRelatedField(
        read_only=True
    )

    class Meta:
        model = Consultation
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'is_archived', 'medecin']

    def create(self, validated_data):
        consultation = super().create(validated_data)

        # Sécurité si patient est null
        if consultation.patient:
            consultations = Consultation.objects.filter(
                patient=consultation.patient,
                medecin=consultation.medecin,
                is_archived=False
            ).order_by('-created_at')

            for c in consultations[MAX_CONSULTATIONS_VISIBLES:]:
                c.is_archived = True
                c.save()

        return consultation
