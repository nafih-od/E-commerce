
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .models import UserProfile
from .forms import UserRegistrationForm, UserLoginForm






def register_user(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Auto-login after registration
            return redirect("dashboard")
    else:
        form = UserRegistrationForm()
    return render #(request, "accounts/register.html", {"form": form})

def login_user(request):
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(request, email=email, password=password)
            if user:
                login(request, user)
                return redirect("dashboard")
    else:
        form = UserLoginForm()
    return render #(request, "accounts/login.html", {"form": form})

def logout_user(request):
    logout(request)
    return redirect("login")

def user_profile(request):
    profile = UserProfile.objects.get(user=request.user)
    return render #(request, "accounts/profile.html", {"profile": profile})

