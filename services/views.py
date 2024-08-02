from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def index(request):
 return render(request,'services/index.html')



# manage error page not found(404)

def error_404(request,exception):
 return render(request,'services/404.html',status=404)