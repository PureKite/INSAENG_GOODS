from django.shortcuts import render, redirect
from django.http import Http404
from django.http import HttpResponse
from .forms import PostForm, Post_ImageForm
from .models import Post, PostImage
from accounts.models import Account
import logging
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
import datetime

logger = logging.getLogger('mylogger')
 
def CreatePost(request):
    logger.error(request.user)
    if not request.user.is_authenticated:
        return redirect('mainapp:main')
    if request.method == 'POST' and request.FILES['Board_image']:
        post_form = PostForm(request.POST)
        post_imageform = Post_ImageForm(request.POST, request.FILES)
        # image = request.FILES['Board_image']
        images = request.FILES.getlist('Board_image')
        if post_form.is_valid():
            user_id = request.user
            user = Account.objects.get(username = user_id)
            p_form = Post(
                Board_share = post_form.cleaned_data['Board_share'],
                Board_gtype = post_form.cleaned_data['Board_gtype'],
                Board_title = post_form.cleaned_data['Board_title'],
                Board_content = post_form.cleaned_data['Board_content'],
                Board_writer = user,
            )
            p_form.save()
            post = Post.objects.last()
            for image in images:
                PostImage.objects.create(
                    Post = post,
                    Board_image = image
                )    
            return redirect('mainapp:main')
        #return render(request, 'Create_Post.html',  {'post_form': post_form, 'post_imageform' : post_imageform})
    else:
        post_form = PostForm()
        post_imageform = Post_ImageForm()
    return render(request, 'Create_Post.html',  {'post_form': post_form, 'post_imageform' : post_imageform})
    
def DetailPost(request, postid):
    if not request.user.is_authenticated:
        return redirect('mainapp:main')
    post = get_object_or_404(Post, Board_id=postid)
    imagelist = PostImage.objects.filter(Post=postid)
    
    if imagelist.exists():
        return render(request, 'Detail_Post.html', {'post':post, 'imagelist':imagelist, 'postid':postid})
    else:
        return Http404('해당 게시물을 찾을 수 없습니다.')
    
def DeletePost(request, postid):
    if not request.user.is_authenticated:
        return redirect('mainapp:main')
    post = get_object_or_404(Post, Board_id=postid)
    post.delete()
    return redirect('mainapp:main')

def UpdatePost(request, postid):
    if not request.user.is_authenticated:
        return redirect('mainapp:main')
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

def ListPost(request):
    login_session = request.session.get('login_session', '')
    context = {'login_session':login_session}
    return render(request, 'List_Post.html', context)

def input_test(request):
    if request.POST:
        list_item = request.POST.getlist('test')
        print(list_item)
        
def page(request):
    board_list = Post.objects.all()
    page = request.GET.get('page', '1')
    paginator = Paginator(board_list, '10')
    page_obj = paginator.page(page)
    return render(request, 'template_name', {'page_obj':page_obj})