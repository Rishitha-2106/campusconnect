import random
from django.conf import settings
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CustomUserCreationForm
from .models import CustomUser
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib.auth import authenticate, login, logout

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            request.session['temp_user'] = {
                'username': form.cleaned_data['username'],
                'email': form.cleaned_data['email'],
                'year': form.cleaned_data['year'],
                'department': form.cleaned_data['department'],
                'password': form.cleaned_data['password1'],
            }
            otp = str(random.randint(100000, 999999))
            request.session['otp'] = otp
            # ✅ Send OTP email
            send_mail(
                subject="CampusConnect Email Verification OTP",
                message=f"Your OTP is {otp}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[form.cleaned_data['email']],
            )
            return redirect('users:verify_otp')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

def verify_otp(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        if entered_otp == request.session.get('otp'):
            data = request.session.get('temp_user')
            if data:
                user = CustomUser.objects.create_user(
                    username=data['username'],
                    email=data['email'],
                    year=data['year'],
                    department=data['department'],
                    password=data['password'],
                    is_verified=True
                )
                messages.success(request, "Account created and verified successfully! Please log in.")
                request.session.pop('temp_user', None)
                request.session.pop('otp', None)
                return redirect('users:login')
        else:
            messages.error(request, "Incorrect OTP. Please try again.")
    return render(request, 'users/verify_otp.html')

@login_required
def dashboard_view(request):
    if not request.user.is_verified and not request.user.is_superuser:
        return HttpResponseForbidden("Access denied: Your email is not verified.")
    return render(request, 'users/dashboard.html', {'user': request.user})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_superuser:
                # For superuser, skip OTP verification
                login(request, user)
                return redirect('users:dashboard')
            # For normal users, check OTP verification
            if user.is_verified:
                login(request, user)
                return redirect('users:dashboard')
            else:
                messages.error(request, 'Please verify your email with OTP first.')
                return redirect('users:verify_otp')
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('users:login')
    return render(request, 'users/login.html')

def logout_view(request):
    logout(request)
    return redirect('users:login')