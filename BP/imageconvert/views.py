from django.shortcuts import render
from .models import *
import numpy as np
import cv2, joblib,sys
import logging
import string
import os
import tf_slim as slim
import tensorflow.compat.v1 as tf
from django.http import FileResponse
from django.core.files.storage import FileSystemStorage
from pathlib import Path
from tqdm import tqdm
from pathlib import Path
from accounts.models import Account
from rembg import remove
from PIL import Image, ImageOps, ImageFilter
from django.contrib.auth.decorators import login_required

def rembg(in_img,output_img):  #input_img: 원본 이미지 경로 /  output_img: 저장 경로 / white_img: 흰 배경 이미지 경로
    
  input_path = in_img
  input = Image.open(input_path)
  output = remove(input)
  ROOT_PATH = str(Path(__file__).resolve().parent.parent)
  background = Image.open(ROOT_PATH + '\\static\\img\\design\\white.jpg')
  logging.warning(background)
  foreground = output
  (img_h, img_w) = foreground.size
  
  resize_back =  background.resize((img_h, img_w))
  resize_back.paste(foreground, (0, 0), foreground)
  img = np.array(resize_back)

  image_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  #b,g,r = cv2.split(img)

  blur = cv2.GaussianBlur(image_gray, ksize=(5,5), sigmaX=0)
  #ret, thresh1 = cv2.threshold(blur, 127, 255, cv2.THRESH_BINARY)
  edged = cv2.Canny(blur, 10, 250)
  kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7,7))
  closed = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)
  contours, _ = cv2.findContours(closed.copy(),cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
  #total=0
  contours_xy = np.array(contours)
  contours_xy.shape
  x_min, x_max = 0,0
  value = list()
  for i in range(len(contours_xy)):
      for j in range(len(contours_xy[i])):
          value.append(contours_xy[i][j][0][0])
          x_min = min(value)
          x_max = max(value)
  # print(x_min)
  # print(x_max)

  y_min, y_max = 0,0
  value = list()
  for i in range(len(contours_xy)):
      for j in range(len(contours_xy[i])):
          value.append(contours_xy[i][j][0][1])
          y_min = min(value)
          y_max = max(value)
  # print(y_min)
  # print(y_max)

  x = x_min
  y = y_min
  w = x_max-x_min
  h = y_max-y_min

  fi_img = output.crop((x,y,x+w,y+h))
  fi_img.save(output_img)
  
  print(fi_img)
  print("돌아갔음")
  #return output_img



def resize_crop(image):
    h, w, c = np.shape(image)
    if min(h, w) > 720:
        if h > w:
            h, w = int(720*h/w), 720
        else:
            h, w = 720, int(720*w/h)
    image = cv2.resize(image, (w, h),
                       interpolation=cv2.INTER_AREA)
    h, w = (h//8)*8, (w//8)*8
    image = image[:h, :w, :]
    return image

def tf_box_filter(x, r):
    k_size = int(2*r+1)
    ch = x.get_shape().as_list()[-1]
    weight = 1/(k_size**2)
    box_kernel = weight*np.ones((k_size, k_size, ch, 1))
    box_kernel = np.array(box_kernel).astype(np.float32)
    output = tf.nn.depthwise_conv2d(x, box_kernel, [1, 1, 1, 1], 'SAME')
    return output

def guided_filter(x, y, r, eps=1e-2):
    
    x_shape = tf.shape(x)
    #y_shape = tf.shape(y)

    N = tf_box_filter(tf.ones((1, x_shape[1], x_shape[2], 1), dtype=x.dtype), r)

    mean_x = tf_box_filter(x, r) / N
    mean_y = tf_box_filter(y, r) / N
    cov_xy = tf_box_filter(x * y, r) / N - mean_x * mean_y
    var_x  = tf_box_filter(x * x, r) / N - mean_x * mean_x

    A = cov_xy / (var_x + eps)
    b = mean_y - A * mean_x

    mean_A = tf_box_filter(A, r) / N
    mean_b = tf_box_filter(b, r) / N

    output = mean_A * x + mean_b

    return output    

def resblock(inputs, out_channel=32, name='resblock'):
    
    with tf.variable_scope(name):
        
        x = slim.convolution2d(inputs, out_channel, [3, 3], 
                               activation_fn=None, scope='conv1')
        x = tf.nn.leaky_relu(x)
        x = slim.convolution2d(x, out_channel, [3, 3], 
                               activation_fn=None, scope='conv2')
        
        return x + inputs

def unet_generator(inputs, channel=32, num_blocks=4, name='generator', reuse=False):
    with tf.variable_scope(name, reuse=reuse):
        
        x0 = slim.convolution2d(inputs, channel, [7, 7], activation_fn=None)
        x0 = tf.nn.leaky_relu(x0)
        
        x1 = slim.convolution2d(x0, channel, [3, 3], stride=2, activation_fn=None)
        x1 = tf.nn.leaky_relu(x1)
        x1 = slim.convolution2d(x1, channel*2, [3, 3], activation_fn=None)
        x1 = tf.nn.leaky_relu(x1)
        
        x2 = slim.convolution2d(x1, channel*2, [3, 3], stride=2, activation_fn=None)
        x2 = tf.nn.leaky_relu(x2)
        x2 = slim.convolution2d(x2, channel*4, [3, 3], activation_fn=None)
        x2 = tf.nn.leaky_relu(x2)
        
        for idx in range(num_blocks):
            x2 = resblock(x2, out_channel=channel*4, name='block_{}'.format(idx))
            
        x2 = slim.convolution2d(x2, channel*2, [3, 3], activation_fn=None)
        x2 = tf.nn.leaky_relu(x2)
        
        h1, w1 = tf.shape(x2)[1], tf.shape(x2)[2]
        x3 = tf.image.resize_bilinear(x2, (h1*2, w1*2))
        x3 = slim.convolution2d(x3+x1, channel*2, [3, 3], activation_fn=None)
        x3 = tf.nn.leaky_relu(x3)
        x3 = slim.convolution2d(x3, channel, [3, 3], activation_fn=None)
        x3 = tf.nn.leaky_relu(x3)

        h2, w2 = tf.shape(x3)[1], tf.shape(x3)[2]
        x4 = tf.image.resize_bilinear(x3, (h2*2, w2*2))
        x4 = slim.convolution2d(x4+x0, channel, [3, 3], activation_fn=None)
        x4 = tf.nn.leaky_relu(x4)
        x4 = slim.convolution2d(x4, 3, [7, 7], activation_fn=None)
        
        return x4

@login_required
def imageconvert(request):
    return render(request, 'imageconvert.html')

def downloadFile(request):
    image = Images.objects.last()
    f_image = image.cvt_img.url
    file_name = os.path.dirname(os.path.abspath(os.path.dirname(__file__))) + f_image
    fs = FileSystemStorage(file_name)
    response = FileResponse(fs.open(file_name, 'rb'), content_type='image/png')
    response['Content-Disposition'] = f'attachment; filename={os.path.basename(f_image)}'
    return response

logger = logging.getLogger('mylogger')

def cartoonize(model_path, load_path, save_path):
    try:
        tf.disable_eager_execution()
    except:
        None

    tf.reset_default_graph()
    #ROOT_PATH = str(Path(__file__).resolve().parent.parent)
    input_photo = tf.placeholder(tf.float32, [1, None, None, 3])
    #input_photo = Image.open(ROOT_PATH + '\\static\\img\\cat.jpg')
    print(input_photo)
    network_out = unet_generator(input_photo)
    final_out = guided_filter(input_photo, network_out, r=1, eps=5e-3)

    all_vars = tf.trainable_variables()
    gene_vars = [var for var in all_vars if 'generator' in var.name]
    saver = tf.train.Saver(var_list=gene_vars)
    
    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True
    sess = tf.Session(config=config)

    sess.run(tf.global_variables_initializer())
    saver.restore(sess, tf.train.latest_checkpoint(model_path))
    # load_path = os.path.join(Path(__file__).resolve().parent.parent, 'test_images')
    # save_path = os.path.join(Path(__file__).resolve().parent.parent, 'cartoonized_images')
    image = cv2.imread(load_path)
    image = resize_crop(image)
    batch_image = image.astype(np.float32)/127.5 - 1
    batch_image = np.expand_dims(batch_image, axis=0)
    output = sess.run(final_out, feed_dict={input_photo: batch_image})
    output = (np.squeeze(output)+1)*127.5
    output = np.clip(output, 0, 255).astype(np.uint8)
    cv2.imwrite(save_path, output)
    
    return output

def viewimage(request):
    if request.method == 'POST' and request.FILES['files']:
        file = request.FILES['files']
        images = Images()
        images.user_id = request.user
        images.raw_img = file
        images.save()
        model_select = request.POST.get('model_select')
        load_path = images.raw_img.path
        ROOT_PATH = str(Path(__file__).resolve().parent.parent)
        img_name = load_path.split('\\')[-1]
        save_path = ROOT_PATH + '\\media\\cvt_img\\'  + img_name # 끝 파일이름만 따와서 앞에 폴더명만 변경
        radio_isChecked = request.POST.get('radio_isChecked')
        
        
        
            
        # 모델 로딩
        if model_select in ['arcane', 'origin', 'simpson', 'thearistocats']:
            model_path = ''.join([ROOT_PATH, '\\model\\saved_models_', model_select])
            cartoonize(model_path, load_path, save_path) # 이미지가 곧바로 DB로 저장되는 건지 imagefield에 맞게 저장되는 건지 확인필요
        else :
            pass # 다른 모델
        
        #if radio_isChecked in ['rembg', 'origin']  and radio_isChecked == 'rembg': 
        #    rembg(load_path, save_path)
        #    logging.warning("확인용")
            
            
        
        images.cvt_img = 'cvt_img/' + img_name
        images.save()
        
        if radio_isChecked in ['rembg', 'origin']  and radio_isChecked == 'rembg': 
          rembg(images.cvt_img.path, save_path)
          images.save()
            
        context = {
            'images': images,
        }
            
        return render(request, 'viewimage.html', context)

    # http method의 GET은 처리하지 않는다. 사이트 테스트용으로 남겨둠
    else:
        test = request.GET['test']
        logger.error(('Something went wrong!!',test))
