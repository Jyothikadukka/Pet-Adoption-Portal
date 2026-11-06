from django.urls import path
from . import views

urlpatterns = [

    path(
        'register/',
        views.register,
        name='register'
    ),

    path(
        'login/',
        views.login_view,
        name='login'
    ),

    path(
        'logout/',
        views.logout_view,
        name='logout'
    ),

    path(
    'profile/',
    views.profile,
    name='profile'
),
path(
    "verify-otp/",
    views.verify_otp,
    name="verify_otp"
),
path(
    "resend-otp/",
    views.resend_otp,
    name="resend_otp"
),
path(
    "success/",
    views.success,
    name="success"
),
path(
    "forgot-password/",
    views.forgot_password,
    name="forgot_password"
),

path(
    "verify-reset-otp/",
    views.verify_reset_otp,
    name="verify_reset_otp"
),

path(
    "reset-password/",
    views.reset_password,
    name="reset_password"
),
path(
    "password-success/",
    views.password_success,
    name="password_success"
),
]

