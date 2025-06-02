from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.contrib.auth.models import User, PermissionsMixin


# class BaseVendor(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     email = models.EmailField()
#     company_name = models.CharField(max_length=100)
#     contact_email = models.EmailField()
#     phone_number = models.CharField(max_length=20, blank=True)
#     address = models.TextField(blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

    # class Meta:
    #     abstract = True


from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, BaseUserManager

from base.models import BaseModel


class VendorManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)

class Vendor(AbstractBaseUser, PermissionsMixin, BaseModel):
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # Required for admin panel access
    email = models.EmailField()
    company_name = models.CharField(max_length=100)
    contact_email = models.EmailField()
    preferred_shipping_partner = models.CharField(max_length=100, blank=True, null=True)
    return_policy = models.TextField(blank=True, null=True)
    support_contact = models.CharField(max_length=100, blank=True, null=True)

    objects = VendorManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["company_name", "phone_number"]

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="vendor_groups",  # Custom related_name to avoid conflict
        blank=True
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="vendor_permissions",  # Custom related_name to avoid conflict
        blank=True
    )

    class Meta:
        db_table = "vendors"
        verbose_name = "Vendor"
        verbose_name_plural = "Vendors"



    def _str_(self):
        return self.company_name
