from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from tenants.models import Tenant,TenantUser

from django.contrib.auth.decorators import login_required

def workspace_dashboard(request, tenant_id):
    if not TenantUser.objects.filter(user=request.user, tenant_id=tenant_id).exists():
        return render(request, "403.html")
    return render(request, "collaboration/dashboard.html", {"tenant_id": tenant_id})

def create_channel_page(request, tenant_id):
    return render(request, "collaboration/create_channel.html", {
        "tenant_id": tenant_id
    })
    

