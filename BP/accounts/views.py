from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate, update_session_auth_hash
from accounts.forms import SignupForm, AccountAuthForm, CustomUserChangeForm, CustomPasswordChangeForm, CheckPasswordForm
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
 
 
def signup(request, *args, **kwargs):
    user = request.user
    if user.is_authenticated:
        return redirect("mainapp:main")
 
    context = {}
    if request.POST:
        form = SignupForm(request.POST)
        print(form)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username').lower()
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(username=username, password=raw_password)
            auth_login(request, account)
            destination = get_redirect_if_exists(request)
            if destination:
                return redirect(destination)
            return redirect("mainapp:main")
        else:
            context['registration_form'] = form
    else:
        form = SignupForm()
        context['registration_form'] = form
 
    return render(request, 'accounts/signup.html', context)
 
 
def logout(request):
    auth_logout(request)
    return redirect("/")
 
 
def login(request, *args, **kwargs):
    context = {}
 
    user = request.user
    if user.is_authenticated:
        return redirect("mainapp:main")
 
    destination = get_redirect_if_exists(request)
    if request.POST:
        form = AccountAuthForm(request.POST)
        if form.is_valid():
            print('??')
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user:
                auth_login(request, user)
                if destination:
                    return redirect(destination)
                return redirect("mainapp:main")
    else:
        form = AccountAuthForm()
    print('111')
    context['login_form'] = form
 
    return render(request, "accounts/login.html", context)
 
 
def get_redirect_if_exists(request):
    redirect = None
    if request.GET:
        if request.GET.get("next"):
            redirect = str(request.GET.get("next"))
    return redirect

def detail(request, pk):
    User = get_user_model()
    user = get_object_or_404(User, pk=pk)
    context = {
        'user': user
    }
    return render(request, 'accounts/detail.html', context)

@login_required
def update(request, pk):
    print('11')
    if request.method == 'POST':
        print('33')
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            print('as')
            form.save()
            return redirect('accountsapp:detail', pk)
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {
        'form': form
    }
    print('22')
    return render(request, 'accounts/update.html', context)


@login_required
def delete(request):
    if request.method == 'POST':
        form = CheckPasswordForm(request.user, request.POST)
        
        if form.is_valid():
            request.user.delete()
            messages.success(request, "회원탈퇴가 완료되었습니다.")
            auth_logout(request)
            return redirect("mainapp:main")
    else:
        form = CheckPasswordForm(request.user)

    return render(request, 'accounts/delete.html', {'form': form})




def password_change(request, pk):
    if request.method == 'POST':
        password_change_form = CustomPasswordChangeForm(request.user, request.POST)
        if password_change_form.is_valid():
            user = password_change_form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "비밀번호를 성공적으로 변경하였습니다.")
            return redirect('accountsapp:detail', pk)
    else:
        password_change_form = CustomPasswordChangeForm(request.user)

    return render(request, 'accounts/password.html', {'password_change_form':password_change_form})
