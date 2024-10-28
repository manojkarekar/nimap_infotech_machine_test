from rest_framework import serializers
from .models import Client, Project
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class ProjectSerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'project_name', 'client', 'users', 'created_by', 'created_at', 'updated_at']

class CreateProjectSerializer(serializers.ModelSerializer):
    users = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True)

    class Meta:
        model = Project
        fields = ['project_name', 'client', 'users']

class ClientSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(source='created_by.username', read_only=True) 
    projects = ProjectSerializer(many=True, read_only=True)

    class Meta:
        model = Client
        fields = ['id', 'client_name', 'created_by', 'created_at', 'updated_at', 'projects']


class CreateClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'client_name']  
