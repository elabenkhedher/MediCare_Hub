from django.db import models
from django.conf import settings
from patients.models import Patient
from appointments.models import RendezVous

class Consultation(models.Model):

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='consultations'
    )

    medecin = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'medecin'}
    )

    rendez_vous = models.OneToOneField(
        RendezVous,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    diagnostic = models.TextField()
    actes_medicaux = models.TextField(blank=True)
    observations = models.TextField(blank=True)

    is_archived = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Consultation {self.patient} - {self.created_at.date()}"
