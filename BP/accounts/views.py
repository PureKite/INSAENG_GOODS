from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from accounts.forms import SignupForm, AccountAuthForm, CustomUserChangeForm
from django.contrib.auth import get_user_model
 
 
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
            # destination = kwargs.get("next")
            destination = get_redirect_if_exists(request)
            if destination: # if destination != None
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
    print(context)
    return render(request, 'accounts/detail.html', context)

def update(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('articles:index')
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {
        'form': form
    }
    return render(request, 'accounts/update.html', context)