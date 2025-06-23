from django.conf import settings
from django.db import models
import uuid
from brand.models import Brand
from category.models import Category


class Product_type(models.Model):
    screen_size = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    resolution = models.CharField(max_length=50, null=True, blank=True)
    panel_type = models.CharField(max_length=50, null=True, blank=True)
    hdmi_ports = models.PositiveIntegerField(null=True, blank=True)
    usb_ports = models.PositiveIntegerField(null=True, blank=True)
    refresh_rate = models.PositiveIntegerField(null=True, blank=True)
    operating_system = models.CharField(max_length=50, null=True, blank=True)
    energy_rating = models.CharField(max_length=10, null=True, blank=True)
    speaker_type = models.CharField(max_length=50, choices=[("Bluetooth", "Bluetooth"), ("Wired", "Wired")], null=True,
                                    blank=True)
    connectivity = models.CharField(max_length=50, choices=[("Bluetooth", "Bluetooth"), ("AUX", "AUX"), ("USB", "USB"),
                                                            ("Wi-Fi", "Wi-Fi")], null=True, blank=True)
    power_source = models.CharField(max_length=50, choices=[("Battery", "Battery"), ("Wired", "Wired")], null=True,
                                    blank=True)

    def __str__(self):
        return f"{self.panel_type} {self.screen_size} {self.resolution}"  # Customize details based on your needs

    class Meta:
        db_table = "product_types"


class Product(models.Model):
    PRODUCT_TYPES = [
        ('TV', 'TV'),
        ('Speaker', 'Speaker'),
        ('Refrigerator', 'Refrigerator'),
        ('AC', 'AC'),
        ('MOBILE', 'MOBILE')

    ]

    # Common fields
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    product_type = models.ForeignKey(Product_type, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    cover_image = models.ImageField(upload_to="product_images/", null=True, blank=True)
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

    def get_specifications(self):
        """Return all specifications as a dictionary"""
        specs = {}

        # Get specifications from Product_type
        if self.product_type:
            for field in self.product_type._meta.fields:
                if field.name not in ['id']:
                    value = getattr(self.product_type, field.name)
                    if value is not None and value != '':
                        specs[field.verbose_name or field.name] = value

        # Add dynamic properties
        if self.dynamic_properties:
            for key, value in self.dynamic_properties.items():
                specs[key] = value

        return specs

    def __str__(self):
        return f"{self.name} - {self.product_type}"

    class Meta:
        db_table = "products"


class ProductFeatures(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="features")
    features = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.features}"

    class Meta:
        db_table = "product_features"


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images"
    )
    image = models.ImageField(upload_to="product_images/")
    caption = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Image for {self.product.name}"


class Review(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.product.name} - {self.rating}★"
