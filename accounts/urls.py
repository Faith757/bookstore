from django.urls import path
from . import views

urlpatterns=[
    path('homepage', views.HomePage, name="homepage"),
    path('register', views.register, name="register"),
    path('login', views.member_login, name="login"),
    path('Verify-OTP', views.verify_otp, name="verify-OTP"),
    path('edit-profile', views.edit_profile, name='edit-profile'),
    path('logout', views.logout, name="logout"),
]