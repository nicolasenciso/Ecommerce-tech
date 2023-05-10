from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings


class Role(models.Model):
    id_role = models.AutoField(primary_key=True, editable=False)
    ROLE_OPTION = (('admin', 'admin'), ('employee', 'employee'))
    name_role = models.CharField(max_length=50, choices=ROLE_OPTION)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class UserManager(BaseUserManager):

    def create_user(self, user_email, password=None, **extra_fields):
        if not user_email:
            raise ValueError('Users must have an email address')

        user = self.model(user_email=self.normalize_email(user_email), **extra_fields)
        user.set_password(password)
        user.is_active = True
        user.save(using=self._db)

        return user

    def create_superuser(self, user_email, password):
        user = self.create_user(user_email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    id_user = models.AutoField(primary_key=True, editable=False)
    user_name = models.CharField(max_length=255, blank=False, null=False)
    user_email = models.EmailField(max_length=255, unique=True)
    user_surname = models.CharField(max_length=255, blank=False, null=False)
    user_identification = models.CharField(max_length=20, blank=False, null=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, )

    objects = UserManager()

    USERNAME_FIELD = 'user_email'


class ProductType(models.Model):
    id_product_type = models.AutoField(primary_key=True, editable=False)
    name_product_type = models.CharField(max_length=255, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Manufacturer(models.Model):
    id_manufacturer = models.AutoField(primary_key=True, editable=False)
    manufacturer_name = models.CharField(max_length=255, blank=False, null=False)
    manufacturer_nit = models.CharField(max_length=255, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Product(models.Model):
    id_product = models.AutoField(primary_key=True, editable=False)
    name_product = models.CharField(max_length=255, blank=False, null=False)
    price_product = models.DecimalField(decimal_places=2, blank=False, default=0.00, max_digits=10)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, )
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE, )
    amount_product = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Client(models.Model):
    id_client = models.AutoField(primary_key=True, editable=False)
    client_name = models.CharField(max_length=255, blank=False, null=False)
    client_ID = models.CharField(max_length=20, blank=False, null=False)
    client_surname = models.CharField(max_length=255, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Purchase(models.Model):
    id_purchase = models.AutoField(primary_key=True, editable=False)
    total_cost_purchase = models.DecimalField(decimal_places=2, max_digits=10, default=0.00)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ClientProducts(models.Model):
    id_client_product = models.AutoField(primary_key=True, editable=False)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, )
    product = models.ForeignKey(Product, on_delete=models.CASCADE, )
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



