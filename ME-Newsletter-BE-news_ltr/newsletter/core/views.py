from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.db import connections
from django.db.utils import OperationalError
from django.utils import timezone
import os


@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """
    Health check endpoint for monitoring service status
    
    Returns:
        Response: JSON response with service health status
    """
    # Check database connectivity
    db_status = "healthy"
    db_details = {}
    
    try:
        db_conn = connections['default']
        db_conn.cursor()
        db_details = {
            "engine": db_conn.settings_dict.get('ENGINE', 'unknown'),
            "name": db_conn.settings_dict.get('NAME', 'unknown'),
            "host": db_conn.settings_dict.get('HOST', 'localhost'),
        }
    except OperationalError as e:
        db_status = "unhealthy"
        db_details = {"error": str(e)}
    
    # Check if debug mode is enabled (security indicator)
    debug_enabled = os.environ.get('DJANGO_DEBUG', 'False').lower() == 'true'
    
    # Prepare response data
    health_data = {
        "status": "healthy" if db_status == "healthy" else "degraded",
        "timestamp": timezone.now().isoformat(),
        "services": {
            "database": {
                "status": db_status,
                "details": db_details
            },
            "application": {
                "status": "healthy",
                "version": "1.0.0",
                "debug": debug_enabled
            }
        }
    }
    
    # Return appropriate status code
    status_code = status.HTTP_200_OK if db_status == "healthy" else status.HTTP_503_SERVICE_UNAVAILABLE
    
    return Response(health_data, status=status_code)


@api_view(['GET'])
@permission_classes([AllowAny])
def api_status(request):
    """
    API status endpoint for Lovable integration verification
    
    Returns:
        Response: JSON response confirming API availability
    """
    return Response({
        "service": "ME Newsletter API",
        "status": "operational",
        "version": "v1",
        "documentation": "/api/docs/",
        "timestamp": timezone.now().isoformat()
    })