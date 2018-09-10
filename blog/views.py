from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from .models import User
from django.conf import settings
from django.views.generic import View, FormView
from django.contrib.auth import login, authenticate, REDIRECT_FIELD_NAME
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect


from . forms import SignInLikeUsername,SignInLikeEmailForm, SignInLikeEmailorUserForm


class Guest(View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_auntificated:
            return redirect(settings.LOGIN_REDIRECT_URL)
        return super().dispatch(request, *args, **kwargs)


class LogIn(Guest, FormView):
    template_name = 'blog/login.html'

    @staticmethod
    def get_form_class(**kwargs):
        if settings.DISABLE_USERNAME or settings.LOGIN_VIA_EMAIL:
            return SignInLikeEmailForm

        if settings.LOGIN_VIA_EMAIL_OR_USERNAME:
            return SignInLikeEmailorUserForm

        return SignInLikeUsername

    @method_decorator(sensitive_post_parameters('password'))
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        request.session.set_test_cookie()
        return super().dispatch(request, *args, **kwargs)
