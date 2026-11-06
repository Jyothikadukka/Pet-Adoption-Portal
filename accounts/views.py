from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm, ProfileForm, UserUpdateForm
from django.contrib.auth.decorators import login_required
from adoption.models import AdoptionRequest
from .models import Profile
from .forms import ProfileForm
from django.contrib import messages
import random
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime, timedelta


def register(request):

    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():

            otp = str(random.randint(100000, 999999))

            request.session["register_data"] = {
    "username": form.cleaned_data["username"],
    "email": form.cleaned_data["email"],
    "password": form.cleaned_data["password"],
    "otp": otp,
    "otp_time": str(timezone.now())
}

            send_mail(
    subject="Verify Your Pet Adoption Portal Account",

    message=f"""
Hello {form.cleaned_data["username"]},

Welcome to Pet Adoption Portal 🐾

Thank you for registering with us.

To complete your registration, please verify your email address using the OTP below:

--------------------------------

Your Verification OTP: {otp}

--------------------------------

This OTP is valid for 5 minutes.

If you did not create this account, please ignore this email.

Thank you for choosing adoption and helping pets find loving homes ❤️

Regards,
Pet Adoption Portal Team
""",

    from_email=settings.EMAIL_HOST_USER,

    recipient_list=[
        form.cleaned_data["email"]
    ],

    fail_silently=False,
)

            messages.success(
                request,
                "OTP has been sent to your email."
            )

            return redirect("verify_otp")

    else:

        form = RegisterForm()

    return render(
        request,
        "accounts/register.html",
        {
            "form": form
        }
    )


def login_view(request):

    print("LOGIN VIEW IS RUNNING")


    if request.method == "POST":

        username = request.POST.get('username')
        password = request.POST.get('password')


        user = authenticate(
            request,
            username=username,
            password=password
        )


        if user is not None:

            login(request, user)

            return redirect('home')


        else:

            return render(
                request,
                'accounts/login.html',
                {
                    'error':
                    'Invalid username or password'
                }
            )


    return render(
        request,
        'accounts/login.html'
    )



def logout_view(request):

    logout(request)

    return render(
        request,
        'accounts/logout.html'
    )

@login_required
def profile(request):

    profile, created = Profile.objects.get_or_create(
        user=request.user
    )


    requests = AdoptionRequest.objects.filter(
        user=request.user
    )


    user_form = UserUpdateForm(
        instance=request.user
    )


    profile_form = ProfileForm(
        instance=profile
    )


    if request.method == "POST":


        # Username / Email update
        if "user_update" in request.POST:


            user_form = UserUpdateForm(
                request.POST,
                instance=request.user
            )


            if user_form.is_valid():

                user_form.save()

                messages.success(
                    request,
                    "Profile updated successfully"
                )

                return redirect('profile')



        # Phone update
        elif "phone_update" in request.POST:


            profile_form = ProfileForm(
                request.POST,
                instance=profile
            )


            if profile_form.is_valid():

                profile_form.save()

                messages.success(
                    request,
                    "Phone number updated successfully"
                )

                return redirect('profile')



    return render(
        request,
        'accounts/profile.html',
        {
            'requests': requests,
            'profile': profile,
            'form': profile_form,
            'user_form': user_form
        }
    )

def verify_otp(request):

    data = request.session.get("register_data")

    if not data:
        return redirect("register")


    if request.method == "POST":

        entered_otp = request.POST.get("otp")


        # OTP expiry check
        otp_time = datetime.fromisoformat(
            data["otp_time"]
        )

        current_time = timezone.now()

        difference = current_time - otp_time


        if difference > timedelta(minutes=5):

            messages.error(
                request,
                "OTP expired. Please request a new OTP."
            )


        elif entered_otp == data["otp"]:

            user = User.objects.create_user(
                username=data["username"],
                email=data["email"],
                password=data["password"]
            )


            del request.session["register_data"]


            messages.success(
                request,
                "Registration Successful."
            )


            return redirect("success")


        else:

            messages.error(
                request,
                "Invalid OTP."
            )


    return render(
        request,
        "accounts/verify_otp.html",
        {
            "email": data["email"]
        }
    )
def success(request):

    return render(
        request,
        "accounts/success.html"
    )

def resend_otp(request):

    data = request.session.get("register_data")

    if not data:
        return redirect("register")


    new_otp = str(random.randint(100000,999999))


    data["otp"] = new_otp
    data["otp_time"] = str(timezone.now())


    request.session["register_data"] = data


    send_mail(
        subject="Your New Pet Adoption Portal OTP",

        message=f"""
Hello {data["username"]},

Your new verification OTP is:

{new_otp}

This OTP is valid for 5 minutes.

Thank you,
Pet Adoption Portal Team
""",

        from_email=settings.EMAIL_HOST_USER,

        recipient_list=[
            data["email"]
        ],

        fail_silently=False,
    )


    messages.success(
        request,
        "New OTP sent successfully."
    )


    return redirect("verify_otp")

def forgot_password(request):

    if request.method == "POST":

        email = request.POST.get("email")


        try:

            user = User.objects.get(
                email=email
            )


        except User.DoesNotExist:

            messages.error(
                request,
                "Email not registered."
            )

            return redirect(
                "forgot_password"
            )


        otp = str(
            random.randint(100000,999999)
        )


        request.session["reset_data"] = {

            "email": email,

            "otp": otp,

            "otp_time": str(
                timezone.now()
            )

        }


        send_mail(

            subject="Pet Adoption Portal Password Reset OTP",

            message=f"""
Hello {user.username},

We received a request to reset your password.

Your password reset OTP is:

{otp}

This OTP is valid for 5 minutes.

If you did not request this, please ignore this email.

Regards,
Pet Adoption Portal Team 🐾
""",

            from_email=settings.EMAIL_HOST_USER,

            recipient_list=[email],

            fail_silently=False

        )


        messages.success(
            request,
            "OTP sent to your email."
        )


        return redirect(
            "verify_reset_otp"
        )


    return render(
        request,
        "accounts/forgot_password.html"
    )

def verify_reset_otp(request):

    data = request.session.get(
        "reset_data"
    )


    if not data:

        return redirect(
            "forgot_password"
        )


    if request.method=="POST":


        entered_otp=request.POST.get(
            "otp"
        )


        otp_time=datetime.fromisoformat(
            data["otp_time"]
        )


        if timezone.now()-otp_time > timedelta(minutes=5):

            messages.error(
                request,
                "OTP expired."
            )


        elif entered_otp == data["otp"]:


            return redirect(
                "reset_password"
            )


        else:

            messages.error(
                request,
                "Invalid OTP."
            )


    return render(
        request,
        "accounts/verify_reset_otp.html"
    )

def reset_password(request):

    data = request.session.get(
        "reset_data"
    )


    if not data:

        return redirect(
            "forgot_password"
        )


    if request.method == "POST":


        password = request.POST.get(
            "password"
        )


        confirm_password = request.POST.get(
            "confirm_password"
        )


        if password != confirm_password:

            messages.error(
                request,
                "Passwords do not match."
            )

            return redirect(
                "reset_password"
            )


        user = User.objects.get(
            email=data["email"]
        )


        user.set_password(
            password
        )


        user.save()



        del request.session[
            "reset_data"
        ]


        return redirect(
            "password_success"
        )



    return render(
        request,
        "accounts/reset_password.html"
    )

def password_success(request):

    return render(
        request,
        "accounts/password_success.html"
    )