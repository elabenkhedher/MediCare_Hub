# patients/serializers.py
from rest_framework import serializers
from .models import Patient, DossierMedical

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['id', 'nom', 'prenom', 'date_naissance', 'sexe', 'telephone', 'adresse', 'contact_urgence', 'created_at']
        read_only_fields = ['id', 'created_at']
class DossierMedicalSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.nom', read_only=True)

    class Meta:
        model = DossierMedical
        fields = ['id', 'patient', 'patient_name', 'antecedents', 'allergies', 'maladies_chroniques', 'notes_medecin', 'last_update']
        read_only_fields = ['id', 'last_update', 'patient_name']
