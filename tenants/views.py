from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Tenant, TenantUser
from .serializers import TenantSerializer,RegisterSerializer
from .permissions import IsAdmin,IsMember,IsOwner


@api_view(['GET'])
def health_check(request):
    return Response({"message": "Backend is working"})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_tenant(request):
    serializer = TenantSerializer(data=request.data)

    if serializer.is_valid():
        tenant = serializer.save()

        # Assign logged-in user as OWNER
        TenantUser.objects.create(
            user=request.user,
            tenant=tenant,
            role='owner'
        )

        return Response({
            "message": "Tenant created successfully",
            "tenant": serializer.data
        }, status=201)

    return Response(serializer.errors, status=400)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_tenants(request):
    tenant_users = TenantUser.objects.filter(user=request.user)
    tenants = [tu.tenant for tu in tenant_users]

    serializer = TenantSerializer(tenants, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        return Response(
            {"message":"User registered successfully"},
            status=201
        )
    return Response(serializer.errors,status=400)

@api_view(['POST'])
@permission_classes([IsAuthenticated,IsOwner])
def change_subscription(request):
    return Response({
        "message": "Subscription chaged (OWNER access)"
    })
    
@api_view(['POST'])
@permission_classes([IsAuthenticated,IsAdmin])
def manage_users(request):
    return Response({
        "message": "User managed (ADMIN/OWNER access)"
    })
    
@api_view(['GET'])
@permission_classes([IsAuthenticated,IsMember])
def view_tasks(request):
    return Response({
        "message": "Tasks fetched (MEMBER access)"
    })
