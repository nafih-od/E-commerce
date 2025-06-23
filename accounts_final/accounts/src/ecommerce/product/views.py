from django.shortcuts import render, get_object_or_404

from product.models import Product


def product(request):
    _product_instance_ = Product.objects.all()
    context = {
        "product_list": _product_instance_,
    }
    return render(request, 'product.html', context)


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    features = Product.features.objects.all()
    return render(request, "product/product_details.html", {
        "product": product,
        "features": features
    })


def compare_products(request):
    # Get all products for dropdowns
    products = Product.objects.all().prefetch_related('features', 'images')

    # Get selected products from GET parameters
    product1_id = request.GET.get('product1')
    product2_id = request.GET.get('product2')

    # Fetch selected products
    product1 = Product.objects.filter(id=product1_id).first() if product1_id else None
    product2 = Product.objects.filter(id=product2_id).first() if product2_id else None

    # Prepare comparison data
    comparison_data = []

    if product1 and product2:
        # Get common specifications
        specs1 = product1.get_specifications()
        specs2 = product2.get_specifications()

        # Get all unique specification keys
        all_keys = sorted(set(specs1.keys()) | set(specs2.keys()))

        # Build comparison data
        for key in all_keys:
            val1 = specs1.get(key, '-')
            val2 = specs2.get(key, '-')
            comparison_data.append({
                'name': key,
                'value1': val1,
                'value2': val2,
                'is_different': str(val1) != str(val2)
            })

    return render(request, 'product/compare.html', {
        'products': products,
        'product1': product1,
        'product2': product2,
        'comparison_data': comparison_data
    })
