from django.shortcuts import render, redirect, get_object_or_404
from .forms import PostForm, Post_ImageForm, CommentForm
from .models import Post, PostImage, Comment
from accounts.models import Account
import logging
from django.core.paginator import Paginator
import datetime
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
logger = logging.getLogger('mylogger')

@login_required
def CreatePost(request):
    logger.error(request.user)
    if request.method == 'POST' and request.FILES['Board_image']:
        post_form = PostForm(request.POST)
        post_imageform = Post_ImageForm(request.POST, request.FILES)
        # image = request.FILES['Board_image']
        images = request.FILES.getlist('Board_image')
        if post_form.is_valid():
            user_id = request.user
            user = Account.objects.get(username = user_id)
            result = ''
            for i in request.POST.getlist('Board_gtype'):
                result += i
                result += ' '
            p_form = Post(
                Board_share = post_form.cleaned_data['Board_share'],
                Board_gtype = result,
                Board_title = post_form.cleaned_data['Board_title'],
                Board_content = post_form.cleaned_data['Board_content'],
                Board_writer = user,
            )
            p_form.save()
            post = p_form
            for image in images:
                PostImage.objects.create(
                    Post = post,
                    Board_image = image
                )    
            return redirect('articleapp:DetailPost',  post.Board_id)
    else:
        post_form = PostForm()
        post_imageform = Post_ImageForm()
    return render(request, 'Create_Post.html',  {'post_form': post_form, 'post_imageform' : post_imageform})

@login_required
def DetailPost(request, postid):
    post = get_object_or_404(Post, Board_id=postid)
    comment = CommentForm()
    return render(request, 'Detail_Post.html', {'post':post, 'comment':comment})

@login_required 
def DeletePost(request, postid):
    post = get_object_or_404(Post, Board_id=postid)
    post.delete()
    return redirect('mainapp:main')

@login_required
def UpdatePost(request, postid):
    post = get_object_or_404(Post, Board_id=postid)
    
    if request.method == 'POST' and request.FILES['Board_image']:
        post_form = PostForm(request.POST)
        post_imageform = Post_ImageForm(request.POST, request.FILES)
        if request.POST.getlist('Board_gtype'):
            post.postimage.all().delete()
            post.Board_share=request.POST['Board_share']
            result = ''
            for i in request.POST.getlist('Board_gtype'):
                result += i
                result += ' '
            # logger.error(result)
            post.Board_gtype=result
            # post.Board_gtype=request.POST.getlist('Board_gtype')
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
            return render(request, 'Update_Post.html', {'post_form': post_form, 'post_imageform' : post_imageform, 'postid':postid})
    else:
        #logger.error( Post.objects.get(Board_id=postid).Board_gtype.split(' '))
        # #post_form = PostForm(initial={'Board_share':post.Board_share, 'Board_gtype': Post.objects.filter(Board_id=postid).values_list('Board_gtype', flat=True),
        #                               })
        post_form = PostForm(instance=post, initial={'Board_gtype': Post.objects.get(Board_id=postid).Board_gtype.split(' ')})
        post_imageform = Post_ImageForm()
        context = {'post_form': post_form, 
                   'post_imageform' : post_imageform, 
                   'postid':postid}
        return render(request, 'Update_Post.html',  context)

@login_required
def CreateComment(request, postid):
    c_form = CommentForm(request.POST)
    if c_form.is_valid():
        user_id = request.user
        user = Account.objects.get(username = user_id)
        post = get_object_or_404(Post, Board_id = postid)
        f_c_form = Comment(
            Comment_post = post,
            Comment_content = c_form.cleaned_data['Comment_content'],
            Comment_writer = user,
        )
        f_c_form.save()
    return redirect('articleapp:DetailPost', postid)

@login_required
@csrf_exempt
def UpdateComment(request):
    data = json.loads(request.body.decode('utf8'))
    comment = Comment.objects.filter(id=data.get('id'))
    context = {
        'result' : 'no',
    }
    if comment is not None:
        comment.update(Comment_content=data.get('Comment_content'), Comment_datetime=datetime.datetime.now())
        context = {
            'result':'ok',
        }
        return JsonResponse(context)
    return JsonResponse(context)
    
@login_required
def DeleteComment(request, postid, commentid):
    comment = get_object_or_404(Comment, pk=commentid)
    comment.delete()
    return redirect('articleapp:DetailPost', postid)

def ListPost(request):
    postlist = Post.objects.all().order_by('-Board_datetime')
    logger.error(postlist)
    imagelist = PostImage.objects.all()
    logger.error(imagelist)
    # login_session = request.session.get('login_session', '')
    # context = {'login_session':login_session}
    return render(request, 'List_Post.html', {'postlist':postlist, 'imagelist':imagelist})#, context)

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