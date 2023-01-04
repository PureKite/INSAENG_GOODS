from django.shortcuts import render
from goods.models import design
import os
from pathlib import Path
from django.http import FileResponse
from django.core.files.storage import FileSystemStorage

import cv2, sys
# from rembg import remove
from PIL import Image, ImageOps, ImageFilter
import numpy as np
from imageconvert.models import Images
# Create your views here.
def makegoods(request):
    image = Images.objects.filter(user_id=request.user.id).last()
    img_path = image.cvt_img
    print("#####@@@@####")
    print(img_path)

    hp = 'static/img/design/hp.jpg'
    gt = 'static/img/design/gt.jpg'
    kr = 'static/img/design/kr.png'
    ts = 'static/img/design/ts.png'

    foreground = Image.open(img_path)
    hp_bg = Image.open(hp)
    gt_bg = Image.open(gt)
    kr_bg = Image.open(kr)
    ts_bg = Image.open(ts)
    try:
        re_hp_img = foreground.resize((200, 200))
        hp_bg.paste(re_hp_img, (225, 250), re_hp_img)
    
        re_gt_img = foreground.resize((295, 295))
        gt_bg.paste(re_gt_img, (200, 200), re_gt_img)
    
        re_kr_img = foreground.resize((240, 240))
        kr_bg.paste(re_kr_img, (130,555), re_kr_img)
    
        re_ts_img = foreground.resize((180, 180))
        ts_bg.paste(re_ts_img, (163, 110), re_ts_img)
        
    except:
        re_hp_img = foreground.resize((200, 200))
        hp_bg.paste(re_hp_img, (225, 250))
    
        re_gt_img = foreground.resize((295, 295))
        gt_bg.paste(re_gt_img, (200, 200))
    
        re_kr_img = foreground.resize((240, 240))
        kr_bg.paste(re_kr_img, (130,555))
    
        re_ts_img = foreground.resize((180, 180))
        ts_bg.paste(re_ts_img, (163, 110))
        
        
    
    img_name = img_path.path.split('\\')[-1]
    ROOT_PATH = str(Path(__file__).resolve().parent.parent)
    hp_save_path = ROOT_PATH + '\\media\\goods_hp\\' + img_name
    gt_save_path = ROOT_PATH + '\\media\\goods_gt\\' + img_name
    kr_save_path = ROOT_PATH + '\\media\\goods_kr\\' + img_name
    ts_save_path = ROOT_PATH + '\\media\\goods_ts\\' + img_name

    designs = design()
    designs.design_user = request.user
    designs.save()
    designs.design_hp = 'goods_hp/' + img_name
    designs.design_gr = 'goods_gt/' + img_name
    designs.design_kr = 'goods_kr/' + img_name
    designs.design_ts = 'goods_ts/' + img_name
    designs.save()

    hp_bg.save(hp_save_path)
    gt_bg.save(gt_save_path)
    kr_bg.save(kr_save_path)
    ts_bg.save(ts_save_path)

    return render(request, 'makegoods.html', {'design': designs})

def downloadFile_hp(request):
    designs = design.objects.filter(design_user_id=request.user.id).last()
    f_p = designs.design_hp 
    
    file_path = os.path.abspath("media/goods_hp")
    file_name = os.path.basename("media/"+ str(f_p))
    
    fs = FileSystemStorage(file_path)
    response = FileResponse(fs.open(file_name, 'rb'))
    response['Content-Disposition'] = 'attachment; filename="HandPhoneCase.jpg"'
    return response

def downloadFile_gr(request):
    designs = design.objects.filter(design_user_id=request.user.id).last()
    f_p = designs.design_gr 
    
    file_path = os.path.abspath("media/goods_gt")
    file_name = os.path.basename("media/"+ str(f_p))
    
    fs = FileSystemStorage(file_path)
    response = FileResponse(fs.open(file_name, 'rb'))
    response['Content-Disposition'] = 'attachment; filename="GripTok.jpg"'
    return response

def downloadFile_kr(request):
    designs = design.objects.filter(design_user_id=request.user.id).last()
    f_p = designs.design_kr
    
    file_path = os.path.abspath("media/goods_kr")
    file_name = os.path.basename("media/"+ str(f_p))
    
    fs = FileSystemStorage(file_path)
    response = FileResponse(fs.open(file_name, 'rb'))
    response['Content-Disposition'] = 'attachment; filename="KeyRing.jpg"'
    return response

def downloadFile_ts(request):
    designs = design.objects.filter(design_user_id=request.user.id).last()
    f_p = designs.design_ts
    
    file_path = os.path.abspath("media/goods_ts")
    file_name = os.path.basename("media/"+ str(f_p))
    
    fs = FileSystemStorage(file_path)
    response = FileResponse(fs.open(file_name, 'rb'))
    response['Content-Disposition'] = 'attachment; filename="T-Shirt.jpg"'
    return response
