
from django.db import models
import uuid

class Product_type(models.Model):
    screen_size = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    resolution = models.CharField(max_length=50, null=True, blank=True)
    panel_type = models.CharField(max_length=50, null=True, blank=True)
    hdmi_ports = models.PositiveIntegerField(null=True, blank=True)
    usb_ports = models.PositiveIntegerField(null=True, blank=True)
    refresh_rate = models.PositiveIntegerField(null=True, blank=True)
    operating_system = models.CharField(max_length=50, null=True, blank=True)
    energy_rating = models.CharField(max_length=10, null=True, blank=True)
    speaker_type = models.CharField(max_length=50, choices=[("Bluetooth", "Bluetooth"), ("Wired", "Wired")], null=True, blank=True)
    connectivity = models.CharField(max_length=50, choices=[("Bluetooth", "Bluetooth"), ("AUX", "AUX"), ("USB", "USB"), ("Wi-Fi", "Wi-Fi")], null=True, blank=True)
    power_source = models.CharField(max_length=50, choices=[("Battery", "Battery"), ("Wired", "Wired")], null=True, blank=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    capacity = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="Capacity in cubic feet")

    def _str_(self):
        return f"{self.panel_type} {self.screen_size}\" {self.resolution}"  # Customize details based on your needs

    class Meta:
        db_table = "product_types"


class Product(models.Model):
    PRODUCT_TYPES = [
        ('TV', 'TV'),
        ('Speaker', 'Speaker'),
        ('Refrigerator', 'Refrigerator'),
        ('AC', 'AC'),
        ('MOBILE', 'MOBILE')
        # New product types can be added without modifying this schema.
    ]

    # Common fields
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    product_type = models.ForeignKey(Product_type, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    brand = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    stock_quantity = models.PositiveIntegerField(default=0)
    release_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Flexible field for product-specific attributes

    dynamic_properties = models.JSONField(
        null=True,
        blank=True,
        help_text=("Store custom fields for each product type. "
                   "For example, a TV may have keys like 'screen_size', 'resolution', etc., "
                   "while a Speaker might have 'speaker_type' or 'connectivity'.")
    )

    def _str_(self):
        return f"{self.name} - {self.product_type}"

    class Meta:
        db_table = "products"


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images"
    )
    image = models.ImageField(upload_to="product_images/")
    caption = models.CharField(max_length=255, blank=True)

    def _str_(self):
        return f"Image for {self.product.name}"