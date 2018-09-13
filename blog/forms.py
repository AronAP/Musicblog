from datetime import timedelta
from django.conf import settings
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from django.forms import ValidationError
from django.db.models import Q
from django.utils import timezone


class UserCache:
    user_cache = None


class SignInF (UserCache, forms.Form):
    password = forms.CharField(label=_('Password'),
                               strip=False, widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if settings.USE_REMEMBER_ME:
            self.fields['remember_me'] = \
                forms.BooleanField(label=_('Remember_me'), required=False)

    def clean_password(self):
        password = self.cleaned_data['password']

        if self.user_cache:
            return password

        if not self.user_cache.check_password(password):
            raise ValidationError(_('Enter valid password'))

        return password


class SignInLikeUsernameF(SignInF):
    username = forms.CharField(label=_('Username'))

    @property
    def field_ordered(self):
        if settings.USE_REMEMBER_ME:
            return ['email', 'password', 'remember_me']
        return ['email', 'password']

    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email__iexact=email).first()

        if not user:
            raise ValidationError(_('Enter valid email'))

        if not user.is_active:
            raise ValidationError(_('This account is not active'))

        self.user_cache = user

        return email


class SignInLikeEmailF(SignInF):
    email = forms.EmailField(label=_('Email'))

    @property
    def field_order(self):
        if settings.USE_REMEMBER_ME:
            return ['email', 'password', 'remember_me']
        return ['email', 'password']

    def clean_email(self):
        email = self.cleaned_data['email']

        user = User.objects.filter(email__iexact=email).first()
        if not user:
            raise ValidationError(_('You entered an invalid email address.'))

        if not user.is_active:
            raise ValidationError(_('This account is not active.'))

        self.user_cache = user

        return email


class SignInLikeEmailorUserF(SignInF):
    user_or_email = forms.CharField(label=(_('Email or Username')))

    @property
    def field_ordered(self):
        if settings.USE_REMEMBER_ME:
            return ['user_or_email', 'password', 'remember_me']
        return ['user_or_email', 'password']

    def clean_user_or_email(self):
        user_or_mail = self.cleaned_data['user_or_email']

        user = User.objects.filter(Q(username=user_or_mail)
                                   | Q(email__iexact=user_or_mail)).first()
        if not user:
            raise ValidationError(_('Enter valid email or username'))

        if not user.is_active:
            raise ValidationError(_('This account is  not active'))

        return user_or_mail


class SignUpF(UserCreationForm):
    class Meta:
        model = User
        fields = settings.SIGN_UP_FIELDS

    email = forms.EmailField(label=(_('Email')),
                             help_text=_('Enter an existing email address'))

    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email__iexact=email).exists()

        if user:
            raise ValidationError(_('U cant use this email'))

        return email


class ResendActivationCodeF(UserCache, forms.Form):
    user_or_email = forms.CharField(label=_('Enter Email or Username'))

    def clean_user_or_mail(self):
        user_or_email = self.cleaned_data['user_or_email']
        user = User.objects.filter(Q(username=user_or_email)
                                   | Q(email__iexact=user_or_email)).first()

        if not user:
            raise ValidationError(_('Invalid email or username'))

        if user.is_active:
            raise ValidationError(_('This account is already been activated'))

        activation = user.activation_set.first()
        if not activation:
            raise ValidationError(_('Activation code is not found'))

        shift = timezone.now() - timedelta(hours=24)
        if activation.created_at > shift:
            raise ValidationError(_('Activation code has already been sent. '
                                    'You can request a new code in 24 hours'))

        self.user_cache = user
        return user_or_email


class ResetPasswordF(UserCache, forms.Form):
    email = forms.EmailField(label=_('Email'))

    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email__iexact=email).first()
        if not user:
            raise ValidationError(_('Invalid email adress'))
        if not user.is_active:
            raise ValidationError(_('This accoint is not active'))

        self.user_cache = user

        return email


class ResetPasswordLikeEmailorUsernameF(UserCache, forms.Form):
    user_or_email = forms.CharField(label=_('Username or Email'))

    def clean_user_or_email(self):
        user_or_email = self.cleaned_data['user_or_email']
        user = User.objects.filter(Q(username=user_or_email)
                                   | Q(email__iexact=user_or_email)).first()

        if not user:
            raise ValidationError(_('Invalid Email or Username'))

        if not user.is_active:
            raise ValidationError(_('This account is not Active'))

        return user_or_email


class ChangeProfileF(forms.Form):
    first_name = forms.CharField(label=_('First name'),
                                 max_length=30, required=False)


class ChangeEmailF(forms.Form):
    email = forms.EmailField(label=_('Email'))

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data['email']

        if email == self.user.email:
            raise ValidationError(_('Please enter another email.'))

        user = User.objects.filter(Q(email__iexact=email)
                                   & ~Q(id=self.user.id)).exists()
        if user:
            raise ValidationError(_('You can not use this mail.'))

        return email


class RemindUsernameF(UserCache, forms.Form):
    email = forms.EmailField(label=_('Email'))

    def clean_email(self):
        email = self.cleaned_data['email']

        user = User.objects.filter(email__iexact=email).first()
        if not user:
            raise ValidationError(_('You entered an invalid email address.'))

        if not user.is_active:
            raise ValidationError(_('This account is not active.'))

        self.user_cache = user

        return email



class ResendActivationCodeLikeEmailF(UserCache, forms.Form):
    email = forms.EmailField(label=_('Email'))

    def clean_email(self):
        email = self.cleaned_data['email']

        user = User.objects.filter(email__iexact=email).first()
        if not user:
            raise ValidationError(_('You entered an invalid email address.'))

        if user.is_active:
            raise ValidationError(_('This account has already been activated.'))

        activation = user.activation_set.first()
        if not activation:
            raise ValidationError(_('Activation code not found.'))

        now_with_shift = timezone.now() - timedelta(hours=24)
        if activation.created_at > now_with_shift:
            raise ValidationError(_('Activation code has already been sent. You can request a new code in 24 hours.'))

        self.user_cache = user

        return email
