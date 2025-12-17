from rest_framework import serializers
from .models import Channel,Message

class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = ['id','name','created_at']
        
class MessageSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    
    class Meta:
        model = Message
        fields = ['id','user','content','created_at']