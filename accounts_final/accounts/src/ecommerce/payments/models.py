import uuid
from django.db import models
from django.conf import settings
from django.utils import timezone
from product.models import Product


class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders")
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    placed_at = models.DateTimeField(default=timezone.now)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Order {self.id} by {self.user.email}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    price_at_time = models.DecimalField(max_digits=10, decimal_places=2)

    def subtotal(self):
        if self.quantity is not None and self.price_at_time is not None:
            return self.quantity * self.price_at_time
        return 0

    def __str__(self):
        return f"{self.quantity}×{self.product.name if self.product else 'Unknown'}"


class DeliveryAddress(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="shipping_address")
    full_name = models.CharField(max_length=100)
    address_line1 = models.CharField("Address Line 1", max_length=255)
    address_line2 = models.CharField("Address Line 2", max_length=255, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField("ZIP / Postal Code", max_length=20)
    country = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.full_name}, {self.city}"
