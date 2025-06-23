from django.shortcuts import render
from products.models import Product

# from ecommerce import settings

def product(request):
    _product_instances= Product.objects.prefetch_related("images").all()
    product_list=[{field.name: getattr(product, field.name) for field in Product._meta.fields} for product in _product_instances]
    context= {
        "product_list" : product_list
    }
    return render(request, 'product.html',context );
