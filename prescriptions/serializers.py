from rest_framework import serializers
from .models import Prescription, PrescriptionItem, Medication

# Serializer pour chaque ligne de médicament
class PrescriptionItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrescriptionItem
        fields = ['id', 'medication', 'dosage', 'duration', 'instructions']
        read_only_fields = ['id']

# Serializer principal pour l’ordonnance
class PrescriptionSerializer(serializers.ModelSerializer):
    # On inclut les items en lecture/écriture
    items = PrescriptionItemSerializer(many=True)

    class Meta:
        model = Prescription
        fields = [
            'id', 'patient', 'doctor', 'consultation', 
            'created_at', 'doctor_signature', 'doctor_stamp', 
            'is_finalized', 'items'
        ]
        read_only_fields = ['id', 'created_at', 'is_finalized']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        # Création de l’ordonnance principale
        prescription = Prescription.objects.create(**validated_data)

        # Création des lignes de médicament
        for item_data in items_data:
            PrescriptionItem.objects.create(prescription=prescription, **item_data)

        return prescription

    def update(self, instance, validated_data):
        # Permet de mettre à jour l’ordonnance et ses items
        items_data = validated_data.pop('items', None)

        # Mettre à jour les champs simples de l’ordonnance
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if items_data is not None:
            # Supprimer les items existants et recréer
            instance.items.all().delete()
            for item_data in items_data:
                PrescriptionItem.objects.create(prescription=instance, **item_data)

        return instance
