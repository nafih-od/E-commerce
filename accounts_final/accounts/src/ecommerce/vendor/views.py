from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from product.views import product
from .forms import ProductForm


def is_vendor(user):
    return hasattr(user, 'vendor_profile')


@login_required
def vendor_dashboard(request):
    if not is_vendor(request.user):
        return redirect('become_vendor')
    vendor = request.user.vendor_profile
    return render(request, 'vendor/vendor_dashboard.html', {'vendor': vendor, 'products': product})


def is_vendor(user):
    return hasattr(user, 'vendor_profile')


@login_required
def add_product(request):
    if not is_vendor(request.user):
        return redirect('become_vendor')

    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.vendor = request.user.vendor_profile
            product.save()
            return redirect('vendor:vendor_dashboard')
    else:
        form = ProductForm()

    return render(request, 'vendor/add_product.html', {
        'product_form': form
    })


def become_vendor(request):
    return render(request, 'register.html')
