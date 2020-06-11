from django.db import models
from django.contrib.auth.models import User


class UserRole(models.Model):
    role_id = models.AutoField(primary_key=True)
    role_name = models.CharField(max_length=255, unique=True, null=True, blank=True)

    def __str__(self):
        return self.role_name


class RoleDetails(User):
    role = models.ForeignKey(UserRole, on_delete=models.PROTECT)
    mobile = models.BigIntegerField(null=True, default=0, blank=True)
    address = models.TextField(max_length=255, null=True, blank=True, default="")
    verify_link = models.CharField(max_length=255, null=True, blank=True, default="")
    image = models.CharField(max_length=255, blank=True, default="", null=True)

    def __str__(self):
        return f'{self.role.role_name} - {self.email}'


class Categories(models.Model):
    c_id = models.AutoField(primary_key=True)
    c_name = models.CharField(unique=True, null=True, blank=True, default="", max_length=50)
    image = models.CharField(null=True, blank=True, default="", max_length=255)

    def __str__(self):
        return self.c_name


class ProductDetails(models.Model):
    p_id = models.AutoField(primary_key=True)
    category = models.ForeignKey(Categories, on_delete=models.SET_NULL, null=True)
    p_name = models.CharField(null=True, blank=True, default="", max_length=255)
    cover_photo = models.CharField(null=True, blank=True, default="", max_length=255)
    photo = models.CharField(null=True, blank=True, default="", max_length=255)
    description = models.TextField(null=True, blank=True, default="", max_length=255)
    price = models.BigIntegerField(null=True, default=0, blank=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return self.p_name


class TemporaryCart(models.Model):
    t_id = models.AutoField(primary_key=True)
    product = models.IntegerField(default=0, null=True, blank=True)
    p_name = models.CharField(max_length=255, default="", null=True, blank=True)
    price = models.BigIntegerField(null=True, blank=True, default=0)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    total_price = models.BigIntegerField(null=True, blank=True, default=0)
    image = models.CharField(null=True, blank=True, default="", max_length=255)


class Sales(models.Model):
    t_id = models.AutoField(primary_key=True)
    u_email = models.EmailField(default="", null=True, blank=True, max_length=255)
    product = models.IntegerField(default=0, null=True, blank=True)
    p_name = models.CharField(max_length=255, default="", null=True, blank=True)
    price = models.BigIntegerField(null=True, blank=True, default=0)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    total_price = models.BigIntegerField(null=True, blank=True, default=0)
    image = models.CharField(null=True, blank=True, default="", max_length=255)


class InvoiceTable(models.Model):
    invoice = models.AutoField(primary_key=True)
    amount = models.BigIntegerField(default=0, null=True, blank=True)
    u_email = models.EmailField(default="", null=True, blank=True, max_length=255)
    status = models.NullBooleanField(default=0)
    token = models.CharField(default="", null=True, blank=True, max_length=255)
