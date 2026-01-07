# patients/serializers.py
from rest_framework import serializers
from .models import Patient, DossierMedical, DocumentMedical

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['id', 'nom', 'prenom', 'date_naissance', 'sexe', 'telephone', 'email', 'adresse', 'contact_urgence_nom', 'contact_urgence_lien', 'contact_urgence_telephone', 'medecin_traitant', 'date_creation', 'statut_patient', 'observations_administratives', 'numero_securite_sociale', 'organisme_assurance', 'numero_assure', 'statut_assurance']
        read_only_fields = ['id', 'date_creation', 'statut_patient']

class DocumentMedicalSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentMedical
        fields = ['id', 'type_document', 'titre', 'fichier', 'date_ajout', 'description']
        read_only_fields = ['id', 'date_ajout']

class DossierMedicalSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.nom', read_only=True)
    documents = DocumentMedicalSerializer(many=True, read_only=True)

    class Meta:
        model = DossierMedical
        fields = [
            'id', 'patient', 'patient_name',
            # Antécédents
            'antecedents_personnels', 'antecedents_familiaux', 'allergies', 'maladies_chroniques',
            # Histoire médicale
            'historique_medical', 'hospitalisations', 'chirurgies', 'intolerances',
            'risques_particuliers', 'reaction_allergique_grave', 'maladies_actuelles',
            'statut_chronique', 'date_diagnostic', 'vaccinations', 'rappels_vaccinaux',
            # Mesures anthropométriques
            'taille', 'poids', 'imc',
            # Signes vitaux
            'tension_arterielle', 'frequence_cardiaque', 'temperature',
            # Examens et résultats
            'examens_biologiques', 'examens_radiologiques', 'resultats_laboratoire',
            'date_dernier_examen',
            # Traitements
            'traitements_en_cours', 'traitements_anterieurs', 'observance_traitement',
            # Notes et suivi
            'notes_medecin', 'commentaires_specialistes', 'plan_suivi',
            # Documents archivés
            'ordonnances_archivees', 'certificats_medicaux', 'comptes_rendus', 'documents_scannes',
            # Métadonnées
            'date_mise_a_jour', 'documents'
        ]
        read_only_fields = ['id', 'date_mise_a_jour', 'patient_name', 'documents']

class PatientRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = Patient
        fields = ['username', 'password', 'password2', 'role']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({'password2': 'Les mots de passe ne correspondent pas'})
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        patient = Patient.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            role=validated_data.get('role', 'patient')
        )
        return patient
