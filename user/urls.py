from django.urls import path
from user import views

urlpatterns = [
    path("login/", views.user_login, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("sign_up/", views.sign_up, name="sign_up"),
    path("forgot_password/", views.forgot_pass, name="forgot_password"),
    path("reset_password/<int:user_id>/", views.reset_pass, name="reset_password"),
]
