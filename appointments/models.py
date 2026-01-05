from django.db import models
from django.conf import settings
from patients.models import Patient

class RendezVous(models.Model):

    STATUS_CHOICES = (
        ('en_attente', 'En attente'),
        ('confirme', 'Confirmé'),
        ('annule', 'Annulé'),
        ('termine', 'Terminé'),
    )

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='rendez_vous'
    )

    medecin = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'medecin'}
    )

    date = models.DateField()
    heure_debut = models.TimeField()
    heure_fin = models.TimeField()

    statut = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='en_attente'
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='rdv_crees'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('medecin', 'date', 'heure_debut')
        ordering = ['date', 'heure_debut']

    def __str__(self):
        return f"{self.patient} - {self.date} {self.heure_debut}"
