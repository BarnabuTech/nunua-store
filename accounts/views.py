# from django.shortcuts import render

# # Create your views here.

from django.shortcuts import render

def user_register(request):
    return render(request, 'account/signup.html')

def user_login(request):
    return render(request, 'account/login.html')
