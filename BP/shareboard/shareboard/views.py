from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.paginator import Paginator
from .forms import *
from .models import *
# Create your views here.
def shareboard(request):
    login_session = request.session.get('login_session', '')
    context = {'login_session':login_session}
    return render(request, 'board/shareboard.html', context)

def input_test(request):
    if request.POST:
        list_item = request.POST.getlist('test')
        print(list_item)
        
def page(request):
    board_list = Board.objects.all()
    page = request.GET.get('page', '1')
    paginator = Paginator(board_list, '10')
    page_obj = paginator.page(page)
    return render(request, 'template_name', {'page_obj':page_obj})