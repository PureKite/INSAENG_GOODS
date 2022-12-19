from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator

def main(request):
    return render(request, 'main/main.html')

def mydesign(request):
    return render(request, 'main/MyDesign.html')


