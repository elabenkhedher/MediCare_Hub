# patients/models.py
from django.db import models

class Patient(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    date_naissance = models.DateField()
    sexe = models.CharField(max_length=10)
    telephone = models.CharField(max_length=20)
    adresse = models.TextField()
    contact_urgence = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

class DossierMedical(models.Model):
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE)
    antecedents = models.TextField(blank=True)
    allergies = models.TextField(blank=True)
    maladies_chroniques = models.TextField(blank=True)
    notes_medecin = models.TextField(blank=True)
    last_update = models.DateTimeField(auto_now=True)
