
from django.urls import path
from . import views

urlpatterns = [
    path('clients/', views.list_clients, name='client_list'),
    path('client/create/', views.create_client, name='create_client'),
    path('client/<int:id>/', views.get_client, name='client_detail'),
    path('client/<int:id>/update/', views.update_client, name='update_client'),
    path('client/<int:id>/delete/', views.delete_client, name='delete_client'),
    path('project/create/', views.create_project, name='create_project'),
    path('user/projects/', views.list_projects_for_user, name='user_projects'),
    
    path('api-token-auth/', views.ObtainAuthToken, name='api-token-auth'),
]
