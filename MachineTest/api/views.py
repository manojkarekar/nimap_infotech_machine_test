from rest_framework import status
from rest_framework.decorators import api_view , permission_classes
from rest_framework.response import Response
from .models import Client, Project
from .serializers import ClientSerializer, ProjectSerializer, CreateClientSerializer, CreateProjectSerializer
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token 
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
import json
from django.http import JsonResponse
from rest_framework.permissions import AllowAny, IsAuthenticated 
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes

# get the all clients with get request
@api_view(['GET'])
def list_clients(request):
    clients = Client.objects.all()
    serializer = ClientSerializer(clients, many=True)
    return Response({"message":"list of all clients retrieved successfully.." , "data": serializer.data},status=status.HTTP_200_OK)


# create a new clients with post request
@csrf_exempt
@api_view(['POST'])
@authentication_classes([TokenAuthentication])  
@permission_classes([IsAuthenticated])  # to check the user is authenticated
def create_client(request):
    serializer = CreateClientSerializer(data=request.data)
    
    if serializer.is_valid():
        client = serializer.save(created_by=request.user)
        return Response({
            'id': client.id, 
            'client_name': client.client_name,
            'created_at': client.created_at,  
            'created_by': request.user.username,
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#get client with the specifice id 
@api_view(['GET'])
def get_client(request, id):
    try:
        client = Client.objects.get(id=id)
        serializer = ClientSerializer(client)
        client_data = serializer.data
        return Response(client_data)
    except Client.DoesNotExist:
        return Response({"message":"client id is not found"},status=status.HTTP_404_NOT_FOUND)


#update client with the specifice id 
@api_view(['PUT', 'PATCH'])
def update_client(request, id):
    try:
        client = Client.objects.get(id=id)
        serializer = CreateClientSerializer(client, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            
            return Response({
                'id': serializer.data['id'],
                'client_name': serializer.data['client_name'],
                'created_at': client.created_at,
                'created_by': client.created_by.username,
                'updated_at': client.updated_at,
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Client.DoesNotExist:
        return Response({"message":"client id is not found"},status=status.HTTP_404_NOT_FOUND)

# delete a client with the specifice id
@api_view(['DELETE'])
def delete_client(request, id):
    try:
        client = Client.objects.get(id=id)
        client.delete()
        return Response({"message":"client is deleted.."},status=status.HTTP_204_NO_CONTENT)
    except Client.DoesNotExist:
        return Response({"message":"client id is not found"},status=status.HTTP_404_NOT_FOUND)

# create a new project and assign to the user
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_project(request):
    serializer = CreateProjectSerializer(data=request.data)
    if serializer.is_valid():
        project  = serializer.save(created_by=request.user)
        project_data = {
            'id': project.id,
            'project_name': project.project_name,
            'client': project.client.client_name,
             'users': [
                {'id': user.id, 'name': user.username} for user in project.users.all() 
            ],
            'created_at': project.created_at,
            'created_by': project.created_by.username if project.created_by else None,
        }
        return Response(project_data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# all projects assign to the logged-in user
@api_view(['GET'])
def list_projects_for_user(request):
    projects = Project.objects.filter(users=request.user)
    serializer = ProjectSerializer(projects, many=True)
    return Response(serializer.data)


# to generate a auth token view
@csrf_exempt
def ObtainAuthToken(request):
    if request.method == 'POST':
        try:
            # Parse the JSON body
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            
            user = authenticate(username=username, password=password)
            if user:
                token, created = Token.objects.get_or_create(user=user)
                return JsonResponse({'token': token.key}, status=200)
            return JsonResponse({'error': 'Invalid Credentials'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    return JsonResponse({'error': 'Method not allowed'}, status=405)