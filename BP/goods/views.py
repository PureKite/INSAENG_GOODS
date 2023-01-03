from django.shortcuts import render
from goods.models import design
import os
from pathlib import Path
from django.http import FileResponse
from django.core.files.storage import FileSystemStorage

import cv2
# from rembg import remove
from imageconvert.models import Images
# Create your views here.

def remove_bg(resizes, img_fg, img_bg, pos_w, pos_h):
    img_fg = cv2.resize(img_fg, resizes)
    _, mask = cv2.threshold(img_fg[:,:,3], 1, 255, cv2.THRESH_BINARY)
    mask_inv = cv2.bitwise_not(mask)

    img_fg = cv2.cvtColor(img_fg, cv2.COLOR_BGRA2BGR)
    h, w = img_fg.shape[:2]
    roi = img_bg[pos_w:pos_w+w, pos_h:pos_h+h]

    masked_fg = cv2.bitwise_and(img_fg, img_fg, mask=mask)
    masked_bg = cv2.bitwise_and(roi, roi, mask=mask_inv)

    added = masked_fg + masked_bg
    img_bg[pos_w:pos_w+w, pos_h:pos_h+h] = added
    
    return img_bg
    

def makegoods(request):
    image = Images.objects.filter(user_id=request.user.id).last()
    img_path = image.cvt_img.path
    img_name = img_path.split('\\')[-1] 
    ROOT_PATH = str(Path(__file__).resolve().parent.parent)
    
    foreground = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
    hp = 'static/img/design/hp.jpg'
    gt = 'static/img/design/gt.jpg'
    kr = 'static/img/design/kr.png'
    ts = 'static/img/design/ts.png'

    hp_bg = cv2.imread(hp)
    gt_bg = cv2.imread(gt)
    kr_bg = cv2.imread(kr)
    ts_bg = cv2.imread(ts)

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

    cv2.imwrite(hp_save_path, remove_bg((200, 200), foreground, hp_bg, 250, 225))
    cv2.imwrite(gt_save_path, remove_bg((295, 295), foreground, gt_bg, 200, 200))
    cv2.imwrite(kr_save_path, remove_bg((240, 240), foreground, kr_bg, 555, 130))
    cv2.imwrite(ts_save_path, remove_bg((180, 180), foreground, ts_bg, 150, 163))

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
