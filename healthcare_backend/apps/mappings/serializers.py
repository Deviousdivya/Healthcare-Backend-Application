from rest_framework import serializers

from apps.doctors.serializers import DoctorSerializer
from .models import PatientDoctorMapping


class MappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientDoctorMapping
        fields = ("id", "patient", "doctor", "created_at")
        read_only_fields = ("id", "created_at")
        validators = []

    def validate_patient(self, patient):
        # Only the user who created a patient may assign doctors to them.
        if patient.created_by_id != self.context["request"].user.id:
            raise serializers.ValidationError("Patient not found.")
        return patient

    def validate(self, attrs):
        if PatientDoctorMapping.objects.filter(patient=attrs["patient"], doctor=attrs["doctor"]).exists():
            raise serializers.ValidationError("This doctor is already assigned to this patient.")
        return attrs


class MappingDetailSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source="patient.name", read_only=True)
    doctor_details = DoctorSerializer(source="doctor", read_only=True)

    class Meta:
        model = PatientDoctorMapping
        fields = ("id", "patient", "patient_name", "doctor", "doctor_details", "created_at")
