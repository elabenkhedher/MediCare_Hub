from rest_framework import serializers
from .models import Prescription, PrescriptionItem, Medication

# Serializer pour chaque ligne de medicament
class PrescriptionItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrescriptionItem
        fields = ['id', 'medication', 'dosage', 'duration', 'instructions']
        read_only_fields = ['id']

# Serializer principal pour l'ordonnance
class PrescriptionSerializer(serializers.ModelSerializer):
    # On inclut les items en lecture/ecriture
    items = PrescriptionItemSerializer(many=True)

    class Meta:
        model = Prescription
        fields = [
            'id', 'patient', 'doctor', 'consultation', 
            'created_at', 'doctor_signature', 'doctor_stamp', 
            'is_finalized', 'items'
        ]
        read_only_fields = ['id', 'created_at', 'is_finalized', 'doctor']
        extra_kwargs = {
            'doctor': {'required': False}
        }

    def create(self, validated_data):
        # Get the doctor from the request user
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['doctor'] = request.user
        
        items_data = validated_data.pop('items')
        # Creation de l'ordonnance principale
        prescription = Prescription.objects.create(**validated_data)

        # Creation des lignes de medicament
        for item_data in items_data:
            PrescriptionItem.objects.create(prescription=prescription, **item_data)

        return prescription

    def update(self, instance, validated_data):
        # Permet de mettre a jour l'ordonnance et ses items
        items_data = validated_data.pop('items', None)

        # Mettre a jour les champs simples de l'ordonnance
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if items_data is not None:
            # Supprimer les items existants et recreer
            instance.items.all().delete()
            for item_data in items_data:
                PrescriptionItem.objects.create(prescription=instance, **item_data)

        return instance
