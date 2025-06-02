# from django.db import models
# import uuid
# from base.models import BaseModel
#
#
# class BaseProduct(BaseModel):
#     # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
#     name = models.CharField(max_length=255)
#     description = models.TextField()
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     brand = models.CharField(max_length=255)
#     category = models.CharField(max_length=255)
#     stock_quantity = models.PositiveIntegerField(default=0)
#     # created_at = models.DateTimeField(auto_now_add=True)
#     # updated_at = models.DateTimeField(auto_now=True)
#
#     class Meta:
#         abstract = True
#
#
# class TV(BaseProduct):
#     screen_size = models.DecimalField(max_digits=5, decimal_places=2)  # eg, 5inches
#     resolution = models.CharField(max_length=50)  # eg, '4K', '1080p'
#     panel_type = models.CharField(max_length=50)  # eg, 'LeD', 'OLEd'
#     smart_tv = models.BooleanField(default=False)
#     hdmi_ports = models.PositiveIntegerField()
#     usb_ports = models.PositiveIntegerField()
#     refresh_rate = models.PositiveIntegerField(help_text='In Hz')
#     operating_system = models.CharField(max_length=50)  # e.g., 'Android TV'
#     energy_rating = models.CharField(max_length=10)  # e.g., 'A++'
#
#     class Meta:
#         db_table = "products_tv"
#         verbose_name = "TV"
#         verbose_name_plural = "TVs"
#
#     def _str_(self):
#         return f"{self.name} - {self.resolution} ({self.screen_size} inches)"
#
#
# class Speaker(BaseProduct):
#     type = models.CharField(max_length=50, choices=[("Bluetooth", "Bluetooth"), ("Wired", "Wired")])
#     connectivity = models.CharField(max_length=50, choices=[("Bluetooth", "Bluetooth"), ("AUX", "AUX"), ("USB", "USB"),
#                                                             ("Wi-Fi", "Wi-Fi")])
#     power_source = models.CharField(max_length=50, choices=[("Battery", "Battery"), ("Wired", "Wired")])
#     frequency_range = models.CharField(max_length=50)  # e.g., '20Hz - 20kHz'
#     weight = models.DecimalField(max_digits=5, decimal_places=2)  # in kg
#     features = models.TextField(blank=True)  # Additional features like waterproofing, noise cancellation
#     release_date = models.DateField(null=True, blank=True)
#     image = models.ImageField(upload_to="speaker_images/", null=True, blank=True)  # Image
#
#     class Meta:
#         db_table = "products_speaker"
#         verbose_name = "Speaker"
#         verbose_name_plural = "Speakers"
#
#     def _str_(self):
#         return f"{self.name} - {self.type} Speaker"
#
#
# class Refrigerator(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     name = models.CharField(max_length=100)
#     brand = models.CharField(max_length=50)
#     capacity = models.DecimalField(max_digits=5, decimal_places=2, help_text="Capacity in cubic feet")
#     door_style = models.CharField(max_length=50, help_text="e.g., French Door, Side-by-Side")
#     energy_rating = models.CharField(max_length=5, help_text="e.g., A++, A+")
#     has_water_dispenser = models.BooleanField(default=False)
#     has_ice_maker = models.BooleanField(default=False)
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     stock_quantity = models.PositiveIntegerField(default=0)
#     created_at = models.DateTimeField(auto_now_add=True)
#     image = models.ImageField(upload_to="Refrigerator_images/", null=True, blank=True)  # Image
#
#     def _str_(self):
#         return f"{self.name} ({self.brand})"
#
#
# class AC(BaseProduct):
#     type = models.CharField(max_length=50, choices=[("Split", "Split"), ("Window", "Window"), ("Portable", "Portable")])
#     capacity = models.DecimalField(max_digits=4, decimal_places=2, help_text="Capacity in Tons")  # e.g., 1.5 Tons
#     energy_rating = models.CharField(max_length=10, choices=[("3 Star", "3 Star"), ("5 Star", "5 Star")])
#     features = models.TextField(blank=True)  # e.g., Inverter, Fast Cooling, Anti-Bacterial Filter
#     noise_level = models.DecimalField(max_digits=4, decimal_places=2, help_text="Noise in dB")
#     release_date = models.DateField(null=True, blank=True)
#     image = models.ImageField(upload_to="ac_images/", null=True, blank=True)  # Image field for AC
#
#     class Meta:
#         db_table = "products_ac"
#         verbose_name = "AC"
#         verbose_name_plural = "ACs"
#
#     def _str_(self):
#         return f"{self.name} - {self.type} AC"

from django.db import models
import uuid


class Product(models.Model):
    PRODUCT_TYPES = [
        ('TV', 'TV'),
        ('Speaker', 'Speaker'),
        ('Refrigerator', 'Refrigerator'),
        ('AC', 'AC'),
    ]

    # Common fields for all products
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    product_type = models.CharField(max_length=50, choices=PRODUCT_TYPES)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    brand = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    stock_quantity = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # TV-specific fields
    screen_size = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # in inches
    resolution = models.CharField(max_length=50, null=True, blank=True)  # e.g., '4K', '1080p'
    panel_type = models.CharField(max_length=50, null=True, blank=True)  # e.g., 'LED', 'OLED'
    smart_tv = models.BooleanField(null=True, blank=True)
    hdmi_ports = models.PositiveIntegerField(null=True, blank=True)
    usb_ports = models.PositiveIntegerField(null=True, blank=True)
    refresh_rate = models.PositiveIntegerField(null=True, blank=True, help_text='In Hz')
    operating_system = models.CharField(max_length=50, null=True, blank=True)
    tv_energy_rating = models.CharField(max_length=10, null=True, blank=True)  # separate from AC energy rating

    # Speaker-specific fields
    speaker_type = models.CharField(
        max_length=50,
        choices=[("Bluetooth", "Bluetooth"), ("Wired", "Wired")],
        null=True,
        blank=True
    )
    connectivity = models.CharField(
        max_length=50,
        choices=[("Bluetooth", "Bluetooth"), ("AUX", "AUX"), ("USB", "USB"), ("Wi-Fi", "Wi-Fi")],
        null=True,
        blank=True
    )
    power_source = models.CharField(
        max_length=50,
        choices=[("Battery", "Battery"), ("Wired", "Wired")],
        null=True,
        blank=True
    )
    frequency_range = models.CharField(max_length=50, null=True, blank=True)  # e.g., '20Hz - 20kHz'
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # in kg
    speaker_features = models.TextField(null=True, blank=True)  # additional features
    speaker_release_date = models.DateField(null=True, blank=True)
    speaker_image = models.ImageField(upload_to="speaker_images/", null=True, blank=True)

    # Refrigerator-specific fields
    capacity = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Capacity in cubic feet"
    )
    door_style = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        help_text="e.g., French Door, Side-by-Side"
    )
    refrigerator_energy_rating = models.CharField(max_length=5, null=True, blank=True)
    has_water_dispenser = models.BooleanField(null=True, blank=True)
    has_ice_maker = models.BooleanField(null=True, blank=True)
    refrigerator_image = models.ImageField(upload_to="refrigerator_images/", null=True, blank=True)

    # AC-specific fields
    ac_type = models.CharField(
        max_length=50,
        choices=[("Split", "Split"), ("Window", "Window"), ("Portable", "Portable")],
        null=True,
        blank=True
    )
    ac_capacity = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Capacity in Tons"
    )
    ac_energy_rating = models.CharField(
        max_length=10,
        choices=[("3 Star", "3 Star"), ("5 Star", "5 Star")],
        null=True,
        blank=True
    )
    ac_features = models.TextField(null=True, blank=True)
    noise_level = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Noise in dB"
    )
    ac_release_date = models.DateField(null=True, blank=True)
    ac_image = models.ImageField(upload_to="ac_images/", null=True, blank=True)

    def _str(self):  # Note: use __str_ (with double underscores)
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