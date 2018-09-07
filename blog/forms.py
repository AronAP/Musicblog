from django.conf import settings
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from django.forms import ValidationError

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