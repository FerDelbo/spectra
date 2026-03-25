from django.shortcuts import render
from django.http import HttpResponse

def prof_view(request):
    return HttpResponse("Hello, this is the prof view!")
# Create your views here.
