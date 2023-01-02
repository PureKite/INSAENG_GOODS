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
    designs = design.objects.filter(design_user=request.user).last()
    image = Images.objects.filter(user_id=request.user.id).last()
    img_path = image.cvt_img

    hp = 'static/img/design/hp.jpg'
    gt = 'static/img/design/gt.jpg'
    kr = 'static/img/design/kr.jpg'
    ts = 'static/img/design/ts.jpg'

    foreground = Image.open(img_path)
    hp_bg = Image.open(hp)
    gt_bg = Image.open(gt)
    kr_bg = Image.open(kr)
    ts_bg = Image.open(ts)

    re_hp_img = foreground.resize((200, 200))
    hp_bg.paste(re_hp_img, (225, 250))

    re_gt_img = foreground.resize((295, 295))
    gt_bg.paste(re_gt_img, (200, 200))

    re_kr_img = foreground.resize((240, 240))
    kr_bg.paste(re_kr_img, (135, 550))

    re_ts_img = foreground.resize((80, 80))
    ts_bg.paste(re_ts_img, (100, 90))

    img_name = img_path.path.split('\\')[-1]
    ROOT_PATH = str(Path(__file__).resolve().parent.parent)
    hp_save_path = ROOT_PATH + '\\media\\goods_hp\\' + img_name
    gt_save_path = ROOT_PATH + '\\media\\goods_gt\\' + img_name
    kr_save_path = ROOT_PATH + '\\media\\goods_kr\\' + img_name
    ts_save_path = ROOT_PATH + '\\media\\goods_ts\\' + img_name

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

def downloadFile(request):
    file_path = os.path.abspath("static/img/")
    file_name = os.path.basename("static/img/test_hp.jpg")
    fs = FileSystemStorage(file_path)
    response = FileResponse(fs.open(file_name, 'rb'))
    response['Content-Disposition'] = 'attachment; filename="test_hp.jpg"'
    return response
