from rest_framework import serializers
from ..models import *

class HostSerializer(serializers.Serializer):
    class Meta:
        model = Host
        fields = ('id', 'name', 'auto', 'active', 'created', 'modified', 'last_seen', )
        read_only_fields = ('id', 'created', 'modified', 'last_seen', )

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name', 'auto', 'created', 'modified', )
        read_only_fields = ('id', 'created', 'modified', )
