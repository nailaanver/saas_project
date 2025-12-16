from django.db import models
from django.contrib.auth.models import User


class Tenant(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
class TenantUser(models.Model):
    ROLE_CHOICES = (
        ('owner','Owner'),
        ('admin','Admin'),
        ('member','Member'),
    )
    
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    tenant = models.ForeignKey(Tenant,on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    
    def __str__(self):
        return f"{self.user.username} - {self.tenant.name}"