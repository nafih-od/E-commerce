from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.core.checks import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login
from account.forms import UserRegistrationForm, UserLoginForm, UserProfileForm
from account.models import UserProfile

from category.models import Category
from product.models import Product
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from vendor.models import Vendor


def login_user(request):
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(request, email=email, password=password)

            if user:
                if not user.is_active:
                    messages.error(request, "Your account is inactive.")
                    return render(request, "accounts/login.html", {"form": form})

                login(request, user)

                if user.role == "vendor":
                    return redirect("vendor:vendor_dashboard")
                else:
                    return redirect("account:index")
            else:
                messages.error(request, "Invalid email or password.")
    else:
        form = UserLoginForm()

    return render(request, "accounts/login.html", {"form": form})


def register_user(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Profile will be created automatically by the signal

            # If the role is vendor, create Vendor details
            if request.POST.get('role') == 'vendor':
                Vendor.objects.create(
                    user=user,
                    license_number=form.cleaned_data.get('license_number', ''),
                    store_name=form.cleaned_data.get('store_name', ''),
                    contact_number=form.cleaned_data.get('contact_number', '')
                )

            login(request, user)
            return redirect("account:index")
    else:
        form = UserRegistrationForm()
    return render(request, "accounts/register.html", {"form": form})





def logout_user(request):
    logout(request)
    return redirect("account:login")

def user_profile(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("dashboard")
    else:
        form = UserRegistrationForm()
    return render (request, "accounts/profile.html", {"form": form})



@login_required
def profile_detail(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    return render(request, "accounts/profile.html", {"profile": user_profile})

@login_required
def edit_profile(request):
    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('account:profile_detail')  # 👈 Redirect to profile view after saving
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'accounts/edit_profile.html', {'form': form})

def index(request):
    product_instance = Product.objects.all()
    category_instance = Category.objects.all()
    context = {
        "product_list": product_instance,
        "category_list": category_instance,
    }
    return render(request, 'index.html', context)


def dashboard_view(request):
    return render(request, "dashboard.html")
