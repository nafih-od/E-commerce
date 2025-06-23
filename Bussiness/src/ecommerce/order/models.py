from django.contrib.auth import get_user_model
from django.db import models

from accounts.models import User
from base.models import BaseModel

# Assuming BaseModel is in core/models.py

ORDER_STATUS_CHOICES = [
    ("PENDING", "Pending"),
    ("PROCESSING", "Processing"),
    ("COMPLETED", "Completed"),
    ("CANCELLED", "Cancelled"),
]

class Order(BaseModel):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    order_number = models.CharField(max_length=20, blank=True)
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default="PENDING")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    notes = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.auto_id:
            last_auto_id = self.__class__.objects.aggregate(models.Max('auto_id'))['auto_id__max'] or 0
            self.auto_id = last_auto_id + 1
        if not self.order_number:
            self.order_number = f"ORD{self.auto_id:05d}"  # e.g., ORD00001
        super().save(*args, **kwargs)


class OrderItem(BaseModel):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = "order"
        verbose_name = "order item"
        verbose_name_plural = "order items"

    @property
    def subtotal(self):
        return self.quantity * self.unit_price

    def __str__(self):
        return f"{self.product_name} (x{self.quantity})"
