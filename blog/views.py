from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from .models import User
from django.conf import settings


def home(request):

    #num_post = Posts.objects.all().count()

    num_user = User.objects.count()  # Метод 'all()' применен по умолчанию.

    # Отрисовка HTML-шаблона blog.html с данными внутри
    # переменной контекста context
    return render(
        request,
        'blog/home.html',
        context={'num_user': num_user,},
    )

def login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = auth.authenticate(username = username, password = password)
    if user is not None and user.is_active:
        auth.login(request, user)
        return HttpResponseRedirect("/account/loggedin/")
    else:
        return HttpResponseRedirect("/account/invalid/")

def logout(request):
    auth.login(request)
    return HttpResponseRedirect("/account/loggedout")

def LogInViev(request):
    template_name = 'blog/login.html'

    @staticmethod
    def get_class(**kwargs):
        if settings.DISABLE_USERNAME or settings.LOGIN_VIA_EMAIL:
            return SignIn
