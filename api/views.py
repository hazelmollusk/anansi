from django.shortcuts import render
from rest_framework import viewsets
from serializers import *
from models import *

# Rest framework viewsets

class HostViewSet(viewsets.ModelViewSet):
    queryset = Host.objects.all()
    serializer_class = HostSerializer

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

