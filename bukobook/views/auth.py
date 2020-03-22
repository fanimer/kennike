from bukobook.models import Userinfo
from django.shortcuts import render, HttpResponseRedirect
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
                error = 'Username is incorrect.'
        except Userinfo.DoesNotExist:
            if len(password) <= 7 or len(password) >= 18:
                error = 'Password is incorrect.'

        if error is None:
            user = Userinfo.objects.create_user(username=username, password=password)
            user.save()
            return HttpResponseRedirect(reverse('bukobook:index'))

        messages.add_message(request, messages.INFO, error)
    return render(request, 'auth/register.html')

@csrf_exempt
def login(request):
    if request.method == 'POST':
        error = None
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
        else:
            error = 'This username or password is incorrect.'
        if error is None:
            return HttpResponseRedirect(reverse('bukobook:index'))
        messages.add_message(request, messages.INFO, error)
    return render(request, 'auth/login.html')

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('bukobook:index'))