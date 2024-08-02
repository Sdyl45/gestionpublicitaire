from django.shortcuts import render

# Create your views here.
def login(request):
    return render(request,'utilisateurs/login.html')

def register(request):
    return render(request, 'utilisateurs/register.html')

def forgot_password(request):
    return render(request, 'utilisateurs/forgot-password.html')
