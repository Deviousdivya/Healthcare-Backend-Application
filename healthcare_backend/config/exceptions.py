from django.db import IntegrityError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    """DRF handler that also turns database integrity errors into 400 responses."""
    response = exception_handler(exc, context)
    if response is None and isinstance(exc, IntegrityError):
        return Response(
            {"detail": "The request conflicts with existing data."},
            status=status.HTTP_400_BAD_REQUEST,
        )
    return response
