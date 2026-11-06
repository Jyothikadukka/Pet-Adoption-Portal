from django import forms
from django.contrib.auth.models import User
from .models import Profile
import re
from django.core.validators import RegexValidator

class RegisterForm(forms.ModelForm):

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class':'form-control',
                'placeholder':'Enter password'
            }
        )
    )


    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
                'placeholder':'Enter username'
            }
        )
    )


    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'class':'form-control',
                'placeholder':'Enter email'
            }
        )
    )


    class Meta:
        model = User

        fields = [
            'username',
            'email',
            'password'
        ]



phone_validator = RegexValidator(
    regex=r'^[6-9]\d{9}$',
    message="Enter a valid 10 digit Indian mobile number"
)


class ProfileForm(forms.ModelForm):

    phone = forms.CharField(
        validators=[
            RegexValidator(
                regex=r'^[6-9]\d{9}$',
                message="Enter a valid 10 digit mobile number"
            )
        ],
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
                'placeholder':'Enter phone number'
            }
        )
    )


    class Meta:
        model = Profile
        fields = [
            "phone"
        ]

    def clean_phone(self):

        phone = self.cleaned_data.get("phone")


        if phone:

            if not phone.isdigit():

                raise forms.ValidationError(
                    "Phone number must contain only digits"
                )


            if len(phone)!=10:

                raise forms.ValidationError(
                    "Phone number must be 10 digits"
                )


        return phone
    

class UserUpdateForm(forms.ModelForm):

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
                'placeholder':'Enter username'
            }
        )
    )


    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'class':'form-control',
                'placeholder':'Enter email'
            }
        )
    )


    class Meta:

        model = User

        fields = [
            "username",
            "email"
        ]