# from django.shortcuts import render
# from django.contrib.auth.models import User, Group
# from rest_framework import viewsets
# # from tutorial.quickstart.serializers import UserSerializer, GroupSerializer
# from quickstart.serializers import UserSerializer, GroupSerializer


# class UserViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows users to be viewed or edited.
#     """
#     queryset = User.objects.all().order_by('-date_joined')
#     serializer_class = UserSerializer


# class GroupViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows groups to be viewed or edited.
#     """
#     queryset = Group.objects.all()
#     serializer_class = GroupSerializer
# # Create your views here.

# appname/views.py
from django.shortcuts import render

from rest_framework import viewsets
from .models import UserAuth
from .serializers import UniversitySerializer

class UniversityViewSet(viewsets.ModelViewSet):
    queryset = UserAuth.objects.all()
    serializer_class = UniversitySerializer