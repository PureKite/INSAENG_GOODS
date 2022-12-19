from django.shortcuts import render
from django.http import HttpResponse
from .import models

def imageconvert(request):
    return render(request,'imageconvert.html')

