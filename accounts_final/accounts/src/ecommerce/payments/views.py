import razorpay
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from razorpay.errors import BadRequestError

from cart.models import TempOrder
from payments.models import Order, OrderItem, DeliveryAddress

client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))


@login_required
def payment_page(request):
    temp_order = TempOrder.objects.filter(user=request.user).order_by('-created_at').first()
    if not temp_order or not temp_order.items.exists():
        return redirect('cart:cart_view')

    # Compute total in rupees and paise
    total_rupees = sum(item.quantity * item.price_at_time for item in temp_order.items.all())
    amount_paise = int(total_rupees * 100)

    # Clamp check: do not exceed Razorpay's default per‑txn limit (₹200,000)
    MAX_LIMIT_RUPEES = 200_000
    if amount_paise > MAX_LIMIT_RUPEES * 100:
        error_msg = (
            f"Order total (₹{total_rupees:,.2f}) exceeds the maximum allowed per payment "
            f"(₹{MAX_LIMIT_RUPEES:,}). Please split your order or contact support."
        )
        return render(request, 'cart/payment.html', {
            'error': error_msg,
            'total_rupees': total_rupees,
        })

    if request.method == "POST":
        try:
            razorpay_order = client.order.create({
                'amount': amount_paise,
                'currency': 'INR',
                'receipt': f'temp_order_{temp_order.id}',
                'notes': {'user_id': str(request.user.id)},
                'payment_capture': '1'
            })
            temp_order.razorpay_order_id = razorpay_order['id']
            temp_order.save()
        except BadRequestError as e:
            return render(request, 'cart/payment.html', {
                'error': "Payment gateway error: " + str(e),
                'total_rupees': total_rupees,
            })

        full_name = f"{request.user.first_name} {request.user.last_name}".strip()
        prefill_name = full_name or request.user.email

        return render(request, 'cart/payment.html', {
            'order_id': razorpay_order['id'],
            'amount': amount_paise,
            'currency': 'INR',
            'key_id': settings.RAZORPAY_KEY_ID,
            'name': 'Your Company Name',
            'description': f'Order #{temp_order.id}',
            'prefill_name': prefill_name,
            'prefill_email': request.user.email,
            'total_rupees': total_rupees,
        })

    # GET
    return render(request, 'cart/payment.html', {
        'total_rupees': total_rupees,
    })


@csrf_exempt
@login_required
def payment_success(request):
    if request.method != "POST":
        return HttpResponseBadRequest("Invalid request method")

    # 1. Verify signature
    razorpay_payment_id = request.POST.get('razorpay_payment_id')
    razorpay_order_id = request.POST.get('razorpay_order_id')
    razorpay_signature = request.POST.get('razorpay_signature')

    params_dict = {
        'razorpay_order_id': razorpay_order_id,
        'razorpay_payment_id': razorpay_payment_id,
        'razorpay_signature': razorpay_signature
    }

    try:
        client.utility.verify_payment_signature(params_dict)
    except razorpay.errors.SignatureVerificationError:
        return HttpResponseBadRequest("Invalid signature!")

    # 2. Fetch the TempOrder by the receipt we used
    temp_order = get_object_or_404(TempOrder, razorpay_order_id=razorpay_order_id)

    # 3. Create final Order
    total_amount = sum(item.quantity * item.price_at_time for item in temp_order.items.all())
    final_order = Order.objects.create(
        user=request.user,
        razorpay_order_id=razorpay_order_id,
        razorpay_payment_id=razorpay_payment_id,
        total_amount=total_amount
    )

    # 4. Copy items
    for ti in temp_order.items.all():
        OrderItem.objects.create(
            order=final_order,
            product=ti.product,
            quantity=ti.quantity,
            price_at_time=ti.price_at_time
        )

    # 5. Save delivery address from POST
    # DeliveryAddress.objects.create(
    #     order=final_order,
    #     full_name=request.POST.get('full_name'),
    #     address_line1=request.POST.get('address_line1'),
    #     address_line2=request.POST.get('address_line2', ''),
    #     city=request.POST.get('city'),
    #     state=request.POST.get('state'),
    #     zip_code=request.POST.get('zip_code'),
    #     country=request.POST.get('country'),
    #     phone_number=request.POST.get('phone_number'),
    # )

    # 6. Delete temp order
    temp_order.delete()

    # 7. Render success page
    return render(request, 'cart/success.html', {'order': final_order})

