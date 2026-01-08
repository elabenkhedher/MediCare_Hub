# patients/permissions.py
from rest_framework import permissions

class IsSecretaire(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'secretaire'

class IsMedecin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'medecin'

class IsPatient(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'patient'


class IsMedecinOrPatientReadOnly(permissions.BasePermission):
    """
    Custom permission to allow:
    - Doctors (medecin): full CRUD access
    - Patients: read-only access to their own data
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        # Doctors have full access
        if request.user.role == 'medecin':
            return True
        
        # Patients have read-only access
        if request.user.role == 'patient':
            return request.method in permissions.SAFE_METHODS
        
        return False
