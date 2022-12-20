from django.shortcuts import render

# Create your views here.
def makegoods(request):
    return render(request, 'makegoods.html')