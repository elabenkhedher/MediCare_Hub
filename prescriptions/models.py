from django.db import models
from django.conf import settings

# Médicaments disponibles
class Medication(models.Model):
    name = models.CharField(max_length=100)
    form = models.CharField(max_length=50)  # tablet, syrup, injection
    standard_dosage = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


# Ordonnance principale
class Prescription(models.Model):
    patient = models.ForeignKey(
        'patients.Patient',
        on_delete=models.CASCADE,
        related_name='prescriptions'
    )
    doctor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'medecin'}
    )
    consultation = models.OneToOneField(
        'consultations.Consultation',
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    doctor_signature = models.BooleanField(default=False)
    doctor_stamp = models.BooleanField(default=False)
    is_finalized = models.BooleanField(default=False)

    def __str__(self):
        return f"Prescription #{self.id} - {self.patient}"


# Chaque médicament associé à une ordonnance
class PrescriptionItem(models.Model):
    prescription = models.ForeignKey(
        Prescription,
        on_delete=models.CASCADE,
        related_name='items'
    )
    medication = models.ForeignKey(
        Medication,
        on_delete=models.PROTECT
    )
    dosage = models.CharField(max_length=50)
    duration = models.CharField(max_length=50)
    instructions = models.TextField()

    def __str__(self):
        return f"{self.medication.name}"
