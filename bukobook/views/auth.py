from bukobook.models import Userinfo
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages, auth
from django.urls import reverse

@csrf_exempt
def register(request):
    if request.method == 'POST':
        error = None
        username = request.POST['username']
        password = request.POST['password']
        try:
            if Userinfo.objects.get(username=username):
                error = '用户名已存在。'
        except Userinfo.DoesNotExist:
            if len(password) <= 7 or len(password) >= 18:
                error = '密码必须在7到18位之间'

        if error is None:
            user = Userinfo.objects.create_user(username=username, password=password)
            user.save()
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
            return redirect('bukobook:index')
        messages.add_message(request, messages.INFO, error)
    return render(request, 'auth/register.html')

@csrf_exempt
def login(request):
    request.session['login_from'] = request.META.get('HTTP_REFERER', '/')
    if request.user.is_authenticated:
        return redirect('bukobook:index')
    if request.method == 'POST':
        error = None
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
        else:
            error = '用户名或密码错误。'
        if error is None:
            return redirect(request.session['login_from'])
        messages.add_message(request, messages.INFO, error)
    return render(request, 'auth/login.html')

def logout(request):
    auth.logout(request)
    return redirect(request.META.get('HTTP_REFERER', '/'))