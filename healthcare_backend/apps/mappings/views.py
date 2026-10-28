from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.patients.models import Patient
from .models import PatientDoctorMapping
from .serializers import MappingDetailSerializer, MappingSerializer


def user_mappings(user):
    return PatientDoctorMapping.objects.filter(patient__created_by=user).select_related("patient", "doctor")


class MappingListCreateView(generics.ListCreateAPIView):
    def get_queryset(self):
        return user_mappings(self.request.user)

    def get_serializer_class(self):
        return MappingSerializer if self.request.method == "POST" else MappingDetailSerializer

    def create(self, request, *args, **kwargs):
        serializer = MappingSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        mapping = serializer.save()
        return Response(MappingDetailSerializer(mapping).data, status=status.HTTP_201_CREATED)


class MappingDetailView(APIView):
    """GET takes a patient id (doctors assigned to that patient); DELETE takes a mapping id."""

    def get(self, request, pk):
        patient = get_object_or_404(Patient, pk=pk, created_by=request.user)
        mappings = user_mappings(request.user).filter(patient=patient)
        return Response(MappingDetailSerializer(mappings, many=True).data)

    def delete(self, request, pk):
        mapping = get_object_or_404(user_mappings(request.user), pk=pk)
        mapping.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
