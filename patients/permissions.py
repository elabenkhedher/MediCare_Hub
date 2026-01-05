# patients/permissions.py
from rest_framework import permissions

class IsSecretaire(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'secretaire'

class IsMedecin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'medecin'
