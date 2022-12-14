from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth import login, authenticate, logout
from accounts.forms import SignupForm, AccountAuthForm
 
 
def signup_view(request, *args, **kwargs):
    user = request.user
    if user.is_authenticated:
        return HttpResponse("You are already authenticated as " + str(user.username))
 
    context = {}
    if request.POST:
        print('11')
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            print(form)
            username = form.cleaned_data.get('username').lower()
            print(username)
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(username=username, password=raw_password)
            login(request, account)
            # destination = kwargs.get("next")
            destination = get_redirect_if_exists(request)
            if destination: # if destination != None
                return redirect(destination)
            return redirect('goods:main')
        else:
            context['registration_form'] = form
    else:
        form = SignupForm()
        context['registration_form'] = form
 
    return render(request, 'accounts/signup.html', context)
 
 
def logout_view(request):
    logout(request)
    return redirect("/")
 
 
def login_view(request, *args, **kwargs):
    context = {}
 
    user = request.user
    if user.is_authenticated:
        return redirect("goods:main")
 
    destination = get_redirect_if_exists(request)
    if request.POST:
        form = AccountAuthForm(request.POST)
        if form.is_valid():
            print('??')
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                if destination:
                    return redirect(destination)
                return redirect("goods:main")
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