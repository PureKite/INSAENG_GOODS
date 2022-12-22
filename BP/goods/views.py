from django.shortcuts import render
from . import models
import os
from django.http import FileResponse
from django.core.files.storage import FileSystemStorage

# Create your views here.
def makegoods(request):
    return render(request, 'makegoods.html')

def downloadFile(request):
    file_path = os.path.abspath("static/img/")
    file_name = os.path.basename("static/img/test_hp.jpg")
    fs = FileSystemStorage(file_path)
    response = FileResponse(fs.open(file_name, 'rb'))
    response['Content-Disposition'] = 'attachment; filename="test_hp.jpg"'
    return response