import razorpay
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseBadRequest, HttpResponse
from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Cart, CartItem, TempOrder, TempOrderItem
from product.models import Product
from django.utils import timezone

client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))


@login_required
def add_to_cart(request, product_id):
    cart, created = Cart.objects.get_or_create(user=request.user)
    product = get_object_or_404(Product, pk=product_id)

    try:
        quantity = int(request.POST.get('quantity', 1))
        if quantity < 1:
            quantity = 1
    except (ValueError, TypeError):
        quantity = 1

    item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
    if item_created:
        item.quantity = quantity
    else:
        item.quantity += quantity
    item.save()

    return redirect("cart:detail")


@login_required
def cart_detail(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    items = cart.items.select_related("product")
    total = sum(item.product.price * item.quantity for item in items)
    return render(request, "cart/detail.html", {
        "cart": cart,
        "items": items,
        "total": total,
    })


@login_required
def confirm_cart(request):
    cart = get_object_or_404(Cart, user=request.user)
    items = cart.items.select_related("product")
    temp_order = TempOrder.objects.create(user=request.user)
    for item in items:
        TempOrderItem.objects.create(
            temp_order=temp_order,
            product=item.product,
            quantity=item.quantity,
            price_at_time=item.product.price
        )

    return redirect('cart:review_temp_order', order_id=str(temp_order.id))


@login_required
def review_temp_order(request, order_id):
    temp_order = get_object_or_404(TempOrder, id=order_id, user=request.user)
    items = temp_order.items.select_related("product")
    total = sum(item.subtotal() for item in items)
    return render(request, "cart/temp_order_review.html", {
        "order": temp_order,
        "items": items,
        "total": total,
    })


@login_required
def place_temp_order(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == "POST":
        quantity = int(request.POST.get("quantity", 1))
        temp_order = TempOrder.objects.create(user=request.user, created_at=timezone.now())

        # Add the product and quantity to TempOrderItem
        TempOrderItem.objects.create(
            temp_order=temp_order,
            product=product,
            quantity=quantity,
            price_at_time=product.price,
        )

        return redirect('cart:cart_view')  # Show order summary or confirmation
    return redirect('product:product_detail', product_id=product.id)


@login_required
def cart_view(request):
    latest_order = TempOrder.objects.filter(user=request.user).order_by('-created_at').first()
    items = latest_order.items.all() if latest_order else []
    total = sum(item.price_at_time * item.quantity for item in items)

    return render(request, "cart/cart_view.html", {
        "items": items,
        "total": total,
    })


@login_required
def remove_item(request, item_id):
    try:
        item = CartItem.objects.get(id=item_id, cart__user=request.user)
        item.delete()
        messages.success(request, "Item removed from cart.")
    except CartItem.DoesNotExist:
        messages.error(request, "Item not found or doesn't belong to your cart.")
    return redirect('cart:detail')  # Adjust if your cart view URL is different
