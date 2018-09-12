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
from django.utils.http import is_safe_url
from django.utils.crypto import get_random_string
from .models import Username
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.tokens import default_token_generator
from .utils import (
    send_act_email, send_reset_password_email, send_forgotten_username_email, send_act_change_email,
)


from . forms import SignInLikeUsernameF,SignInLikeEmailF, SignInLikeEmailorUserF, SignUpF, \
    ResendActivationCodeLikeEmailF, ResendActivationCodeF, ResetPasswordLikeEmailorUsernameF, \
    ResetPasswordF,


class GuestV(View):
    #dispatch - check http , take request and some info
    def dispatch(self, request, *args, **kwargs):
        #check for auntification
        if request.user.is_auntificated:
            return redirect(settings.LOGIN_REDIRECT_URL)
        #send to login page
        return super().dispatch(request, *args, **kwargs)
    #super - for parents


class LogInV(GuestV, FormView):
    template_name = 'blog/login.html'
    #load template

    @staticmethod
    #staticmethod like function but whithout self
    def get_form_class(**kwargs):
        if settings.DISABLE_USERNAME or settings.LOGIN_VIA_EMAIL:
            return SignInLikeEmailF

        if settings.LOGIN_VIA_EMAIL_OR_USERNAME:
            return SignInLikeEmailorUserF

        return SignInLikeUsernameF

    @method_decorator(sensitive_post_parameters('password'))
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        request.session.set_test_cookie()
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        request = self.request

        if request.session.test_cookie_worked():
            request.session.delete_test_cookie()

        if settings.USE_REMEMBER_ME:
            if not form.cleaned_data['remember_me']:
                request.session.set_expiry(0)

        login(request, form.user_cache)

        redirect_to = request.POST.get(REDIRECT_FIELD_NAME, request.GET.get(REDIRECT_FIELD_NAME))
        url_safe = is_safe_url(redirect_to, allowed_hosts=request.get_host(), require_https=request.is_secure())

        if url_safe:
            return redirect(redirect_to)

        return redirect(settings.LOGIN_REDIRECT_URL)


class SignUpV(GuestV, FormView):
    template_name = 'blog/sign_up.html'
    form_class = SignUpF

    def form_valid(self, form):
        request = self.request
        user = form.save(commit = False)

        if settings.DISABLE_USERNAME:
            user.username = get_random_string()

        else:
            user.username = form.cleaned_data['username']

        if settings.ENABLE_USER_ACTIVATION:
            user.is_active = False

        user.save()

        if settings.DISABLE_USERNAME:
            user.username = f'user_{user_id}'
            user.save()

        if settings.ENABLE_USER_ACTIVATION:
            code = get_random_string(20)

            act = Username()
            act.code = code
            act.user = user
            act.save()

            send_act_email(request, user.mail, code)

            messages.success(
                request, _('You are signed up. To activate the account, '
                           'follow the link sent to the mail.'))
        else:
            raw_password = form.cleaned_data['new_password']

            user = authenticate(username=user.username, password=raw_password)
            login(request, user)

            messages.success(request, _('U are sign up!'))

        return redirect('home')


class ActivateV(View):
    @staticmethod
    def get(request, code):
        act = get_object_or_404(Username, code=code)

        #lets activate profile
        user = act.user
        user.is_active
        user.save()

        act.delete()

        messages.success(request, _('U have successfully activated your account'))

        return redirect('blog:log_in')


class ResendActivCodeV(GuestV, FormView):
    template_name = 'blog/resend_activation_code.html'

    @staticmethod
    def get_form_class(**kwargs):
        if settings.DISABLE_USERNAME:
            return ResendActivationCodeLikeEmailF

        return ResendActivationCodeF

    def form_valid(self, form):
        user = form.user_cache

        activation = user.activation_set.first()
        activation.delete()

        code = get_random_string(20)

        act = Username()
        act.code = code
        act.user = user
        act.save()

        send_act_email(self.request, user.email, code)

        messages.success(self.request, _('A new activation code has been sent to your email address.'))

        return redirect('blog:resend_activation_code')


class RestorePasswordV(GuestV, FormView):
    template_name = 'blog/restore_password.html'

    @staticmethod
    def get_form_class(**kwargs):
        if settings.RESTORE_PASSWORD_VIA_EMAIL_OR_USERNAME:
            return ResetPasswordLikeEmailorUsernameF

        return ResetPasswordF

    def form_valid(self, form):
        user = form.user_cache
        token = default_token_generator.make_token(user)
        

