import os

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.models import User
import pandas as pd
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


# Create your views here.
def Index(request):
    if request.method == 'POST':
        email = request.POST.get('InputEmail')
        password = request.POST.get('InputPassword')
        UserModel = get_user_model()
        mail_user = UserModel.objects.get(email=email)
        user = authenticate(request, username=mail_user, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'system_admin/auth-login-basic.html')
    else:
        return render(request, 'system_admin/auth-login-basic.html')


def Dashboard(request):
    return render(request, 'system_admin/dashboard.html')


def UserList(request):
    users = User.objects.all()
    return render(request, 'system_admin/users.html', {'users': users})


def CreateUser(request):
    if request.method == 'POST':
        user_exist = User.objects.filter(username=request.POST.get('InputUsername'))
        if user_exist:
            return render(request, 'system_admin/create_user.html', {'msg': 'User already exist !!'})
        else:
            user = User.objects.create_user(
                request.POST.get('InputUsername'),
                request.POST.get('exampleInputEmail'),
                request.POST.get('inputPassword')
            )

            user.first_name = request.POST.get('InputFirstName')
            user.last_name = request.POST.get('InputLastName')

            if request.POST.get('InputIsSuperUser') == 'on':
                user.is_superuser = True
                user.is_staff = True
            else:
                user.is_superuser = False
            if request.POST.get('InputIsStaffUser') == 'on':
                user.is_staff = True
            else:
                user.is_staff = False
            user.save()
            if user:
                return redirect('users')
    return render(request, 'system_admin/create_user.html')


def CreateVoter(request):
    return render(request, 'system_admin/create_voter.html')


@api_view(['POST'])
def FileUpload(request):
    if request.method == 'POST':
        voter_file = request.FILES['voter_file']
        file_type = voter_file.content_type.split('/')[1]
        col_count = 0
        col_list = []
        if file_type == 'csv':
            voter_data = pd.read_csv(voter_file, low_memory=False)
            row_value_list = voter_data.fillna('')
            row_value_list = row_value_list.values.tolist()
            for vDt in voter_data:
                col_list.append(str(col_count))
                col_count = col_count + 1

            return Response({'row_value_list': row_value_list, 'cols': col_list}, status=status.HTTP_200_OK)
        elif file_type == 'vnd.openxmlformats-officedocument.spreadsheetml.sheet':
            voter_data = pd.read_excel(voter_file)
            voter_data.to_csv("temp.csv")
            tmp_csv = pd.read_csv("temp.csv", low_memory=False)
            row_value_list = tmp_csv.fillna('')
            for vDt in voter_data:
                col_list.append(str(col_count))
                col_count = col_count + 1
            os.remove("temp.csv")
            row_value_list = row_value_list.values.tolist()
            return Response({'row_value_list': row_value_list, 'cols': col_list}, status=status.HTTP_200_OK)
    return Response("Error", status=status.HTTP_400_BAD_REQUEST)


def ImportVoter(request):
    if request.method == 'POST' and request.FILES['formFile']:
        voter_file = request.FILES['formFile']
        file_type = voter_file.content_type.split('/')[1]
        col_count = 0
        col_list = []

        if file_type == 'csv':
            voter_data = pd.read_csv(voter_file, low_memory=False)
            row_value_list = voter_data.values.tolist()
            for vDt in voter_data:
                col_list.append(str(col_count))
                col_count = col_count + 1

            page = request.GET.get('page', 1)
            paginator = Paginator(row_value_list, 1000)
            try:
                row_value_list = paginator.page(page)
            except PageNotAnInteger:
                row_value_list = paginator.page(1)
            except EmptyPage:
                row_value_list = paginator.page(paginator.num_pages)

            return render(request, 'system_admin/import_voter.html', {'voter_data': row_value_list, 'cols': col_list})
        elif file_type == 'vnd.openxmlformats-officedocument.spreadsheetml.sheet':
            voter_data = pd.read_excel(voter_file)
            voter_data.to_csv("temp.csv")
            tmp_csv = pd.read_csv("temp.csv", low_memory=False)
            for vDt in tmp_csv:
                col_list.append(str(col_count))
                col_count = col_count + 1
            os.remove("temp.csv")
            row_value_list = tmp_csv.values.tolist()
            return render(request, 'system_admin/import_voter.html', {'voter_data': row_value_list, 'cols': col_list})
        else:
            return render(request, 'system_admin/import_voter.html', {'msg': "File formate error!!! .csv and xlsx is "
                                                                             "acceptable"})
    return render(request, 'system_admin/import_voter.html')


def Voter(request):
    return render(request, 'system_admin/voters.html')
