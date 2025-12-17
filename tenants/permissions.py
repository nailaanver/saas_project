from rest_framework.permissions import BasePermission
from .models import TenantUser


class IsOwner(BasePermission):
    def has_permission(self, request, view):
        tenant_id = request.headers.get('X-Tenant-ID')
        if not tenant_id:
            return False
        
        return TenantUser.objects.filter(
            user = request.user,
            tenant_id = tenant_id,
            role = 'owner'
        ).exists()
        
class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        tenant_id = request.headers.get('X-Tenant-ID')
        if not tenant_id:
            return False
        
        return TenantUser.objects.filter(
            user=request.user,
            tenant_id=tenant_id,
            role='admin'
        ).exists()


class IsMember(BasePermission):
    def has_permission(self, request, view):
        tenant_id = request.headers.get('X-Tenant-ID')
        if not tenant_id:
            return False

        return TenantUser.objects.filter(
            user=request.user,
            tenant_id=tenant_id
        ).exists()
    
class IsOwnerOrAdmin(BasePermission):
    def has_permission(self, request, view):
        tenant_id = request.headers.get('X-Tenant-ID')
        if not tenant_id:
            return False

        tenant_id = int(tenant_id)  # ✅ VERY IMPORTANT

        return TenantUser.objects.filter(
            user=request.user,
            tenant_id=tenant_id,
            role__in=['owner', 'admin']
        ).exists()