from django.shortcuts import render, redirect
from user.forms import EditForm, ChangePasswordForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages


# Create your views here.
@login_required
def update_profile(req):
    user = req.user
    if req.method == "POST":
        form = EditForm(req.POST, req.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = EditForm(instance=user)
    return render(req, "edit_profile.html", {"form": form})


@login_required
def change_pass(req):
    user = req.user
    if req.method == "POST":
        form = ChangePasswordForm(user, req.POST)
        if form.is_valid():
            old_password = form.cleaned_data["old_password"]
            new_password1 = form.cleaned_data["new_password1"]
            new_password2 = form.cleaned_data["new_password2"]

            if not user.check_password(old_password):
                messages.error(
                    req,
                    "Your Old Password Did Not Match, Please enter Correct Password",
                )
            elif new_password1 != new_password2:
                messages.error(
                    req, "Your New Pasword And Confirm Password Did Not Match"
                )
            else:
                user.set_password(new_password1)
                user.save()
                update_session_auth_hash(req, user)
                return redirect("home")
        else:
            messages.error(req, "please Correct The Errors Below")
    else:
        form = ChangePasswordForm(user)
    return render(req, "change_password.html", {"form": form})
