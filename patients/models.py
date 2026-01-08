# patients/models.py
from django.db import models
from django.utils import timezone
from django.conf import settings


class Patient(models.Model):
    SEXE_CHOICES = [
        ('M', 'Masculin'),
        ('F', 'Féminin'),
        ('A', 'Autre'),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name='patient')
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    date_naissance = models.DateField(null=True, blank=True)
    sexe = models.CharField(max_length=1, choices=SEXE_CHOICES, null=True, blank=True)
    telephone = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    adresse = models.TextField(null=True, blank=True)

    medecin_traitant = models.CharField(max_length=150, blank=True)

    contact_urgence_nom = models.CharField(max_length=100, null=True, blank=True)
    contact_urgence_lien = models.CharField(max_length=50, null=True, blank=True)
    contact_urgence_telephone = models.CharField(max_length=20, null=True, blank=True)

    password = models.CharField(max_length=128, blank=True)  # mot de passe hashé
    date_creation = models.DateTimeField(default=timezone.now)
    statut_patient = models.CharField(max_length=20, default='actif')
    observations_administratives = models.TextField(blank=True)

    # Assurance fields
    numero_securite_sociale = models.CharField(max_length=50, blank=True)
    organisme_assurance = models.CharField(max_length=150, blank=True)
    numero_assure = models.CharField(max_length=50, blank=True)
    STATUT_ASSURANCE_CHOICES = [
        ('actif', 'Actif'),
        ('inactif', 'Inactif'),
        ('en_attente', 'En attente'),
    ]
    statut_assurance = models.CharField(max_length=20, choices=STATUT_ASSURANCE_CHOICES, default='en_attente')

    role = models.CharField(max_length=20, default='patient')  # patient / secretaire / medecin

    def __str__(self):
        return f"{self.nom} {self.prenom}"


class DossierMedical(models.Model):
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE, related_name="dossier")

    antecedents_personnels = models.TextField(blank=True)
    antecedents_familiaux = models.TextField(blank=True)
    allergies = models.TextField(blank=True)
    maladies_chroniques = models.TextField(blank=True)

    # Histoire médicale
    historique_medical = models.TextField(blank=True)
    hospitalisations = models.TextField(blank=True)
    chirurgies = models.TextField(blank=True)
    intolerances = models.TextField(blank=True)
    risques_particuliers = models.TextField(blank=True)
    reaction_allergique_grave = models.BooleanField(default=False)
    maladies_actuelles = models.TextField(blank=True)
    statut_chronique = models.BooleanField(default=False)
    date_diagnostic = models.DateField(null=True, blank=True)
    vaccinations = models.TextField(blank=True)
    rappels_vaccinaux = models.TextField(blank=True)

    # Mesures anthropométriques
    taille = models.FloatField(null=True, blank=True)
    poids = models.FloatField(null=True, blank=True)
    imc = models.FloatField(null=True, blank=True)

    # Signes vitaux
    tension_arterielle = models.CharField(max_length=50, blank=True)
    frequence_cardiaque = models.IntegerField(null=True, blank=True)
    temperature = models.FloatField(null=True, blank=True)

    # Examens et résultats
    examens_biologiques = models.TextField(blank=True)
    examens_radiologiques = models.TextField(blank=True)
    resultats_laboratoire = models.TextField(blank=True)
    date_dernier_examen = models.DateField(null=True, blank=True)

    # Traitements
    traitements_en_cours = models.TextField(blank=True)
    traitements_anterieurs = models.TextField(blank=True)
    observance_traitement = models.CharField(max_length=100, blank=True)

    # Notes et suivi
    notes_medecin = models.TextField(blank=True)
    commentaires_specialistes = models.TextField(blank=True)
    plan_suivi = models.TextField(blank=True)
    date_mise_a_jour = models.DateTimeField(auto_now=True)

    # Documents archivés
    ordonnances_archivees = models.TextField(blank=True)
    certificats_medicaux = models.TextField(blank=True)
    comptes_rendus = models.TextField(blank=True)
    documents_scannes = models.TextField(blank=True)

    def __str__(self):
        return f"Dossier médical - {self.patient}"


class DocumentMedical(models.Model):
    TYPE_DOCUMENT = [
        ('ORDONNANCE', 'Ordonnance'),
        ('CERTIFICAT', 'Certificat médical'),
        ('COMPTE_RENDU', 'Compte rendu'),
        ('DOCUMENT', 'Document scanné'),
    ]

    dossier_medical = models.ForeignKey(DossierMedical, on_delete=models.CASCADE, related_name="documents")
    type_document = models.CharField(max_length=20, choices=TYPE_DOCUMENT)
    titre = models.CharField(max_length=200)
    fichier = models.FileField(upload_to='documents_medicaux/')
    date_ajout = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.type_document} - {self.titre}"
