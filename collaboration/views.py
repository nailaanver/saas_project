from django.shortcuts import render
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from tenants.permissions import IsOwnerOrAdmin,IsTenantMember


from .models import Channel,Message
from .serializers import ChannelSerializer,MessageSerializer
from tenants.models import Tenant,TenantUser
from tenants.permissions import IsOwnerOrAdmin

@api_view(['POST'])
@permission_classes([IsAuthenticated, IsOwnerOrAdmin])
def create_channel(request):
    tenant_id = request.headers.get('X-Tenant-ID')
    if not tenant_id:
        return Response({"error": "X-Tenant-ID header missing"}, status=400)

    tenant_id = int(tenant_id)
    name = request.data.get('name')

    if not name:
        return Response({"error": "Channel name required"}, status=400)

    if Channel.objects.filter(tenant_id=tenant_id, name=name).exists():
        return Response({"error": "Channel already exists"}, status=400)

    channel = Channel.objects.create(
        name=name,
        tenant_id=tenant_id,
        created_by=request.user
    )

    return Response(ChannelSerializer(channel).data, status=201)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_channels(request):
    tenant_id = request.headers.get('X-Tenant-ID')
    if not tenant_id:
        return Response({"error": "X-Tenant-ID missing"}, status=400)

    tenant_id = int(tenant_id)  # ✅ REQUIRED

    if not TenantUser.objects.filter(
        tenant_id=tenant_id,
        user=request.user
    ).exists():
        return Response({"error":"Not a tenant member"}, status=403)

    
    channels = Channel.objects.filter(tenant_id=tenant_id)
    return Response(ChannelSerializer(channels,many=True).data)

@api_view(['POST'])
@permission_classes([IsAuthenticated, IsTenantMember])
def send_message(request):
    tenant_id = request.headers.get('X-Tenant-ID')
    if not tenant_id:
        return Response({"error": "X-Tenant-ID missing"}, status=400)

    tenant_id = int(tenant_id)

    # ✅ ANY TENANT MEMBER CAN MESSAGE
    if not TenantUser.objects.filter(
        tenant_id=tenant_id,
        user=request.user
    ).exists():
        return Response(
            {"error": "You are not a member of this workspace"},
            status=403
        )

    channel_id = request.data.get('channel_id')
    content = request.data.get('content')

    if not content:
        return Response({"error": "Message required"}, status=400)

    try:
        channel = Channel.objects.get(
            id=channel_id,
            tenant_id=tenant_id
        )
    except Channel.DoesNotExist:
        return Response({"error": "Invalid channel"}, status=404)

    message = Message.objects.create(
        tenant_id=tenant_id,
        channel=channel,
        user=request.user,
        content=content
    )

    return Response(
        MessageSerializer(message).data,
        status=201
    )

    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_messages(request):
    tenant_id = request.headers.get('X-Tenant-ID')
    channel_id = request.query_params.get('channel_id')

    if not tenant_id or not channel_id:
        return Response(
            {"error": "X-Tenant-ID header and channel_id query param are required"},
            status=400
        )

    tenant_id = int(tenant_id)       # ✅ FIX
    channel_id = int(channel_id)     # ✅ FIX

    messages = Message.objects.filter(
        tenant_id=tenant_id,
        channel_id=channel_id
    ).order_by('created_at')

    return Response(
        MessageSerializer(messages, many=True).data
    )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def debug_auth(request):
    tenant_id = request.headers.get('X-Tenant-ID')

    return Response({
        "logged_in_user": request.user.username,
        "tenant_id_header": tenant_id,
        "tenant_roles": list(
            TenantUser.objects.filter(user=request.user)
            .values("tenant_id", "role")
        )
    })
    
def login_page(request):
    return render(request, "login.html")