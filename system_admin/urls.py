from django.urls import path
from .views import *

urlpatterns = [
    path('', Index, name='index'),
    path('dashboard/', Dashboard, name='dashboard'),
    path('users/', UserList, name='users'),
    path('user/create_user/', CreateUser, name='create_user'),
    path('voter/', Voter, name='voters'),
    path('voter/import_voter/', ImportVoter, name='import_voter'),
    path('voter/create_voter/', CreateVoter, name='create_voter'),
    path('voter/file_upload', FileUpload, name='file_upload'),
]
