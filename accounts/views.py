import secrets
from datetime import timedelta

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import send_mail
from django.utils import timezone
from django.conf import settings
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from .models import OTP, Member
from .forms import Login, verification
from django.db import transaction

User = get_user_model()

# Create your views here.
def HomePage(request):
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email').strip().lower()
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        gender = request.POST.get('gender')

        if not(firstname) or not(lastname) or not(email) or not(address) or not(phone) or not(gender):
            messages.error(request, 'Please fill in all fields.')
            return render(request, 'register.html')

        try:
            validate_email(email)

        except ValidationError:
            messages.error(request, 'Please enter a valid email address.')
            return render(request, 'register.html')

        if User.objects.filter(email__iexact=email).exists():
            messages.error(request, 'This email is already registered.')
            return render(request, 'register.html')

        try:
            with transaction.atomic():
                user = User(
                    username=email,
                    first_name=firstname,
                    last_name=lastname,
                    email=email
                )
                user.set_unusable_password()
                user.save()

                profile = Member.objects.create(
                    user=user,
                    address=address,
                    phone=phone,
                    gender=gender
                )

                messages.success(
                    request,
                    'Registration successful!.'
                )
                return redirect('login')

        except Exception:
            messages.error(request, 'Something went wrong. Please try again.')

    return render(request, 'register.html')

def member_login(request):
    form = Login(request.POST or None)

    if request.method == 'POST' and form.is_valid():

        email = form.cleaned_data['email'].strip()
        user = User.objects.filter(email__iexact=email, is_active = True).first()

        if user:
            otp = f"{secrets.randbelow(1000000):06d}"

            OTP.objects.filter(user=user, is_used=False).update(is_used=True)

            record = OTP.objects.create(
                user=user,
                code_hash=make_password(otp),
                expires_at=timezone.now() + timedelta(minutes=5)
            )
            try:
                send_mail(
                    'BookNest. Login OTP',
                    f'Hello {user.first_name},\n\n'
                    f'Your verification code is {otp}.\n'
                    'It expires in 5 minutes.\n\n'
                    'Please do not share this code.',
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    fail_silently=False
                )
            
            except Exception as e:
                print("EMAIL SENDING ERROR:", repr(e))
                record.delete()
                messages.error(request, 'Unable to send OTP. Please try again')
                return render(request, 'login.html', {'form': form})
            request.session['otp_id'] = record.id
            return redirect('verify-OTP')
        messages.error(request, 'Email not registered')
    return render(request, 'login.html', {'form': form})

def verify_otp(request):
    record = OTP.objects.filter(
        id = request.session.get('otp_id'),
        is_used = False).select_related('user').first()

    if not record:
        messages.error(request, 'Please request a new OTP')
        return redirect('login')

    form = verification(request.POST or None)

    if request.method == 'POST' and form.is_valid():

        otp = form.cleaned_data['otp']
        if timezone.now() >= record.expires_at or record.attempts >= 5:
            record.is_used = True
            record.save()
            request.session.pop('otp_id', None)
            messages.error(request, 'OTP expired. Request another code.')
            return redirect('login')

        if check_password(otp, record.code_hash):
            record.is_used = True
            record.save()

            request.session.pop('otp_id', None)
            login(request, record.user)

            return redirect('book')

        record.attempts += 1
        if record.attempts >= 5:
            record.is_used = True
            record.save()

            request.session.pop('otp_id', None)

            messages.error(
                request,
                'Too many attempts. Please request a new OTP.'
            )
            return redirect('login')

        record.save()
        messages.error(request, 'Incorrect OTP.')

    return render(request, 'verifyOTP.html', {'form': form})

@login_required
def edit_profile(request):

    profile = get_object_or_404(
        Member,
        user=request.user
    )

    if request.method == 'POST':

        firstname = request.POST.get('firstname', '').strip()
        lastname = request.POST.get('lastname', '').strip()
        email = request.POST.get('email', '').strip().lower()
        phone = request.POST.get('phone', '').strip()
        address = request.POST.get('address', '').strip()

        if not firstname or not lastname or not email:
            messages.error(request, 'Please complete your name and email.')
        
        elif User.objects.exclude(pk=request.user.pk).filter(email__iexact=email).exists():
            messages.error(request, 'This email address is already in use.')

        else:
            request.user.first_name = firstname
            request.user.last_name = lastname
            request.user.email = email
            request.user.username = email
            request.user.save()

            profile.phone = phone
            profile.address = address
            profile.save()

            messages.success(request, 'Your profile has been updated successfully.')

            return redirect('edit-profile')

    context = {
        'profile': profile
    }

    return render(request, 'editprofile.html', context)

def logout(request):
    auth_logout(request)
    messages.success(request, "You have successfully logout")
    return redirect('login')