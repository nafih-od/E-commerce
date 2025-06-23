from django.forms import model_to_dict
from django.shortcuts import render, get_object_or_404

from product.models import Product
from .models import Category


def category_list(request):
    """Retrieve active categories for display."""
    categories = Category.objects.filter(is_active=True).order_by("name")
    return render(request, "category/category.html", {"category_list": categories})


def category_detail(request, slug):
    """Retrieve the selected category and display details."""
    category = get_object_or_404(Category, slug=slug, is_active=True)
    product_instance = Product.objects.filter(category=category)

    context = {
        "category": category,
        "product_list": product_instance,
    }

    return render(request, "category/category_detail.html", context)


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product_fields = model_to_dict(product)
    return render(request, "product/product_details.html", {
        "product": product,
        "product_fields": product_fields
    })
