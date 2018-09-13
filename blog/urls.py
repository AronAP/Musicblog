from django.urls import path
from blog.views import (
    LogInV, ResendActivCodeV, RemindUsernameView, SignUpV, ActivateV, LogOutView,
    ChangeEmailView, ChangeEmailActView, ChangeProfileView, ChangePasswordView,
    RestorePasswordV, RestorePasswordDoneView, RestorePasswordConfirmView,
)

app_name = 'blog'

urlpatterns = [
    path('log-in/', LogInV.as_view(), name='log_in'),
    path('log-out/', LogOutView.as_view(), name='log_out'),

    path('resend/activation-code/', ResendActivCodeV.as_view(), name='resend_activation_code'),

    path('sign-up/', SignUpV.as_view(), name='sign_up'),
    path('activate/<code>/', ActivateV.as_view(), name='activate'),

    path('restore/password/', RestorePasswordV.as_view(), name='restore_password'),
    path('restore/password/done/', RestorePasswordDoneView.as_view(), name='restore_password_done'),
    path('restore/<uidb64>/<token>/', RestorePasswordConfirmView.as_view(), name='restore_password_confirm'),

    path('remind/username/', RemindUsernameView.as_view(), name='remind_username'),

    path('change/profile/', ChangeProfileView.as_view(), name='change_profile'),
    path('change/password/', ChangePasswordView.as_view(), name='change_password'),
    path('change/email/', ChangeEmailView.as_view(), name='change_email'),
    path('change/email/<code>/', ChangeEmailActView.as_view(), name='change_email_activation'),
]