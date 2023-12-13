from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def introduce(request):
    return HttpResponse("Hi My name is Rahul Choudhary")
