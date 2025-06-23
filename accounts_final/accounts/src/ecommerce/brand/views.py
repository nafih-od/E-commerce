from django.shortcuts import render
from brand.models import Brand


def brand(request):
    brand_instance_ = Brand.objects.all()
    context = {
        'brands': brand_instance_,
    }
    return render(request, 'brand/brand.html', context)
