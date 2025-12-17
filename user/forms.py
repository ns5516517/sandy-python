from django import forms
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm


class SignUPForm(forms.ModelForm):
    GENDER = [("M", "Male"), ("F", "Female")]
    first_name = forms.CharField(
        label="First Name",
        max_length=30,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Enter Your First Name"}
        ),
    )
    last_name = forms.CharField(
        label="Last Name",
        max_length=30,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Enter Your Last Name"}
        ),
    )
    email = forms.EmailField(
        label="Email",
        max_length=30,
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Enter Your Email"}
        ),
    )
    password = forms.CharField(
        label="Password",
        min_length=8,
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Enter your password"}
        ),
    )
    contact_number = forms.CharField(
        label="Contact Number",
        max_length=15,
        min_length=10,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Enter Your Phone Number"}
        ),
    )
    gender = forms.ChoiceField(
        choices=GENDER, widget=forms.RadioSelect(attrs={"class": "form-check-input"})
    )

    class Meta:
        model = CustomUser
        fields = [
            "first_name",
            "last_name",
            "email",
            "password",
            "contact_number",
        ]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Email Already exists!")
        return email

    def clean_contact_number(self):
        contact_number = self.cleaned_data.get("contact_number")
        if CustomUser.objects.filter(contact_number=contact_number).exists():
            raise forms.ValidationError("Phone Number Already exists!")
        return contact_number


class LoginForm(forms.Form):
    email = forms.EmailField(
        label="Email",
        max_length=30,
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Enter Your Email"}
        ),
    )
    password = forms.CharField(
        label="Password",
        min_length=8,
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Enter your password"}
        ),
    )


class EditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            "first_name",
            "last_name",
            "email",
            "contact_number",
            "gender",
            "user_image",
        ]
        widgets = {
            "first_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter Your First Name"}
            ),
            "last_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter Your Last Name"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "Enter Your Email"}
            ),
            "contact_number": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter your password"}
            ),
            "gender": forms.Select(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter Your Phone Number",
                }
            ),
            "user_image": forms.FileInput(
                attrs={"class": "edit_icon", "style": "opacity:0;margin:0;"}
            ),
        }


class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Enter Your Old Password"}
        )
    )
    new_password1 = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Enter Your New Password"}
        ),
    )
    new_password2 = forms.CharField(
        label="Confirm New Password",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Confirm Your New Password"}
        ),
    )


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(
        label="Email",
        max_length=30,
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Enter Your Email"}
        ),
    )


class ResetPasswordForm(forms.Form):
    new_password1 = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Enter Your New Password"}
        ),
    )
    new_password2 = forms.CharField(
        label="Confirm New Password",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Confirm Your New Password"}
        ),
    )
