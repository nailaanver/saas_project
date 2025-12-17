from django.db import models
from django.contrib.auth.models import User
from tenants.models import Tenant


class Channel(models.Model):
    name = models.CharField(max_length=100)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('name', 'tenant')
        
    def __str__(self):
        return f"{self.name} ({self.tenant.name})"
    
class Message(models.Model):
    tenant = models.ForeignKey(Tenant,on_delete=models.CASCADE)
    channel = models.ForeignKey(Channel,on_delete=models.CASCADE) 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.content[:30]