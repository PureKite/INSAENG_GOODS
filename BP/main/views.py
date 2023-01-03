from django.shortcuts import render
from article.models import Post, PostImage
import logging
from django.http import HttpResponse
from django.core.paginator import Paginator
logger = logging.getLogger('mylogger')

def main(request):
    postlist = Post.objects.order_by('-Board_id')
    return render(request, 'main/main.html', {'postlist': postlist})