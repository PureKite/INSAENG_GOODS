from django.shortcuts import render

# Create your views here.
def loading(request):
    return render(request, 'loading.html')