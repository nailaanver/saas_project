from rest_framework import serializers
from .models import Tenant,TenantUser
from django.contrib.auth.models import User

class TenantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tenant
        fields = '__all__'
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','email']
        
class TenantUserSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = TenantUser
        fields = ['id','user','tenant','role']
        
class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    tenant_name = serializers.CharField()

    def create(self, validated_data):
        # Create user
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )

        # Create tenant (workspace)
        tenant = Tenant.objects.create(
            name=validated_data['tenant_name']
        )

        # Assign OWNER role
        TenantUser.objects.create(
            user=user,
            tenant=tenant,
            role='owner'
        )

        return user
