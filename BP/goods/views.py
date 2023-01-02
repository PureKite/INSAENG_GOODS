from django.shortcuts import render
from goods.models import design
import os
from django.http import FileResponse
from django.core.files.storage import FileSystemStorage

import cv2, sys
# from rembg import remove
from PIL import Image, ImageOps, ImageFilter
from matplotlib import pyplot as plt
import numpy as np
from imageconvert.models import Images

# Create your views here.
def makegoods(request):
    designs = design.objects.filter(design_user = request.user).last()
    return render(request, 'makegoods.html', {'design':designs})

def downloadFile(request):
    file_path = os.path.abspath("static/img/")
    file_name = os.path.basename("static/img/test_hp.jpg")
    fs = FileSystemStorage(file_path)
    response = FileResponse(fs.open(file_name, 'rb'))
    response['Content-Disposition'] = 'attachment; filename="test_hp.jpg"'
    return response

def autodesign(request):
    image = Images.objects.filter(user_id=request.user.id)
    print(image.values())
    context = {
        'image': image,
    }
    return render(request, 'loading.html', context)
