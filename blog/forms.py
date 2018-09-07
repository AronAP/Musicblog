from django.conf import settings
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from django.forms import ValidationError
from django.db.models import Q

class UserCache:
    user_cache = None

class SignIn(UserCache, forms.Form):
    password = forms.CharField(label = _('Password'), strip = False, widget = forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if settings.USE_REMEMBER_ME:
            self.fields['remember_me'] = forms.BooleanField(label = _('Remember_me'), required = False)

    def clean_password(self):
        password = self.cleaned_data['password']

        if self.user_cache:
            return password

        if not self.user_cache.check_password(password):
            raise ValidationError(_('Enter valid password'))

        return password



class SignInLikeUsername(SignIn):
    username = forms.CharField(label = _('Username'))


    @property
    def field_ordered(self):
        if settings.USE_REMEMBER_ME:
            return ['email', 'password', 'remember_me']
        return ['email', 'password']

    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email__iexact = email).first()

        if not user:
            raise ValidationError(_('Enter valid email'))

        if not user_is_active:
            raise ValidationError(_('This account is not active'))

        self.user_cache = user

        return email

class SignInLikeEmailorUserForm(SignIn):
    user_or_email = forms.CharField(label=(_('Email or Username')))

    @property
    def field_ordered(self):
        if settings.USE_REMEMBER_ME:
            return ['user_or_email', 'password', 'remember_me']
        return ['user_or_email', 'password']

    def clean_user_or_email(self):
        user_or_mail = self.cleaned_data['user_or_email']

        user = User.objects.filter(Q(username=user_or_mail) | Q(email__iexact=user_or_mail)).first()
        if not user:
            raise ValidationError(_('Enter valid email or username'))