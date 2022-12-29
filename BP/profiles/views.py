from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from profiles.models import Profile
from profiles.forms import ProfileForm
from article.models import Post, PostImage
from django.core.paginator import Paginator
from django.contrib import messages


@login_required
def update(request, pk):
    print(pk)
    profile=get_object_or_404(Profile, pk=pk)
    if request.user == profile.user:
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if request.method=='POST':
            if form.is_valid():
                profile.image = form.cleaned_data['image']
                profile.message = form.cleaned_data['message']
                profile.save()
                messages.success(request,"성공적으로 수정되었습니다.")
                return redirect('accountsapp:detail', profile.user.pk)
        else:
            messages.warning(request,"다시 입력하세요")
            form = ProfileForm(instance=profile)

        context={
            'form': form
        }
        return render(request,'profiles/update.html', context)
    else:
        messages.warning(request,"작성자가 아닙니다.")
        return redirect('accountsapp:detail', pk)

@login_required
def mydesign(request):
    post_list = Post.objects.filter(Board_writer_id=request.user.id).order_by('-Board_datetime')

    return render(request, 'profiles/MyDesign.html', {'post_list': post_list})
