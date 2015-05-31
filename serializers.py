from rest_framework import serializers
from .models import *

class HostSerializer(serializers.Serializer):
    class Meta:
        model = Host
        fields = ('name', 'auto', 'active', 'created', 'last_modified', 'last_seen', )

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('name', 'auto', 'created', 'last_modified', )
