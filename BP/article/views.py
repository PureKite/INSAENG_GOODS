from django.shortcuts import render, redirect
from django.http import Http404
from django.http import HttpResponse
from .forms import PostForm, Post_ImageForm
from .models import Post, PostImage
import logging
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.utils import timezone
import datetime

logger = logging.getLogger('mylogger')

def CreatePost(request):
    if request.method == 'POST' and request.FILES['Board_image']:
        post_form = PostForm(request.POST)
        post_imageform = Post_ImageForm(request.POST, request.FILES)
        # image = request.FILES['Board_image']
        images = request.FILES.getlist('Board_image')
        if post_form.is_valid():
            post_form.save(commit=False)
            post_form.save()
            post = Post.objects.last()
            for image in images:
                PostImage.objects.create(
                    Post = post,
                    Board_image = image
                )    
            return redirect('main:main')
        return render(request, 'Create_Post.html',  {'post_form': post_form, 'post_imageform' : post_imageform})
    else:
        post_form = PostForm()
        post_imageform = Post_ImageForm()
        return render(request, 'Create_Post.html',  {'post_form': post_form, 'post_imageform' : post_imageform})
    
def DetailPost(request, postid):
    post = get_object_or_404(Post, Board_id=postid)
    imagelist = PostImage.objects.filter(Post=postid)
    logger.error(imagelist)
    if imagelist.exists():
        return render(request, 'Detail_Post.html', {'post':post, 'imagelist':imagelist, 'postid':postid})
    else:
        return Http404('해당 게시물을 찾을 수 없습니다.')
    
def DeletePost(request, postid):
    post = get_object_or_404(Post, Board_id=postid)
    post.delete()
    return redirect('main:main')

def UpdatePost(request, postid):
    post = get_object_or_404(Post, Board_id=postid)
    imagelist = PostImage.objects.filter(Post=postid)
    
    if request.method == 'POST' and request.FILES['Board_image']:
        post_form = PostForm(request.POST)
        post_imageform = Post_ImageForm(request.POST, request.FILES)
        if request.POST.getlist('Board_gtype'):
            imagelist.delete()
            post.Board_share=request.POST['Board_share']
            post.Board_gtype=request.POST.getlist('Board_gtype')
            post.Board_title=request.POST['Board_title']
            post.Board_content=request.POST['Board_content']
            post.Board_datetime=datetime.datetime.now()
            post.save()
            images = request.FILES.getlist('Board_image')
            for image in images:
                PostImage.objects.create(
                    Post = post,
                    Board_image = image            
                )
            return redirect('/article/detail/'+str(postid))
        else:
            return render(request, 'Update_Post.html', {'post_form': post_form, 'post_imageform' : post_imageform, 'postid' : postid})
    else:
        post_form = PostForm(instance=post)
        post_imageform = Post_ImageForm()
        return render(request, 'Update_Post.html',  {'post_form': post_form, 'post_imageform' : post_imageform, 'postid' : postid})
    