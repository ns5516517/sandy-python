from django.shortcuts import render, redirect
from .forms import SignUPForm, LoginForm, ForgotPasswordForm, ResetPasswordForm
from .models import CustomUser
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout, authenticate
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages


def user_login(req):
    form = LoginForm()
    if req.method == "POST":
        form = LoginForm(req.POST)
        if not form.is_valid():
            print(form.has_error(), "**************")
        else:
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(username=email, password=password)
            if user is not None:
                auth_login(req, user)
                return redirect("home")
            else:
                form.add_error(None, "Invalid Email or Password")

    return render(req, "login.html", {"form": form})


def sign_up(req):
    if req.method == "POST":
        form = SignUPForm(req.POST)
        print(form.is_valid())
        if form.is_valid():
            user = CustomUser.objects.create_user(
                username=form.cleaned_data["email"],
                first_name=form.cleaned_data["first_name"],
                last_name=form.cleaned_data["last_name"],
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password"],
            )
            user.contact_number = form.cleaned_data["contact_number"]
            user.gender = form.cleaned_data["gender"]
            print(user.contact_number, user.gender, "***************************")
            user.save()
            auth_login(req, user)
            return redirect("home")
    else:
        form = SignUPForm()
    return render(req, "sign_up.html", {"form": form})


def forgot_pass(req):
    form = ForgotPasswordForm(req.POST or None)
    if req.method == "POST":
        print("Received POST request")
        if form.is_valid():
            print("Form is valid")
            email = form.cleaned_data["email"]
            try:
                user = CustomUser.objects.get(email=email)
                reset_link = f"http://127.0.0.1:8000/user/reset_password/{user.id}/"
                print(reset_link)

                check = send_mail(
                    subject="Reset Password Link",
                    message=f"Click the link below to reset your password:\n{reset_link}\n\nIf you did not request this, please ignore this email.",
                    recipient_list=[user.email],
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    fail_silently=False,
                )
                print("Email sent successfully!", user.email, check)
                # return redirect("reset_password")
            except CustomUser.DoesNotExist:
                print("Email not found in database")
                form.add_error("email", "Email Not Found")
        else:
            print("Form errors:", form.errors)

    return render(req, "forgot_password.html", {"form": form})


def reset_pass(req, user_id):
    form = ResetPasswordForm(req.POST or None)

    try:
        user = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        messages.error(req, "Invalid reset link or user does not exist.")
        return redirect("forgot_password")

    if req.method == "POST":
        if form.is_valid():
            new_password1 = form.cleaned_data["new_password1"]
            new_password2 = form.cleaned_data["new_password2"]
            print(user.check_password(new_password1))
            if user.check_password(new_password1):
                form.add_error(
                    "new_password1",
                    "The new password should not be the same as the old password.",
                )
            elif new_password1 != new_password2:
                form.add_error("new_password2", "Passwords do not match.")
            else:
                user.set_password(new_password1)
                user.save()
                messages.success(
                    req,
                    "Your password has been reset successfully. You can now log in.",
                )
                return redirect("login")
        else:
            print(form.errors, "---------------")

    return render(req, "reset_password.html", {"form": form})


def logout_view(req):
    logout(req)
    return redirect("home")
