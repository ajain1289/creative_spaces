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
    otp = models.IntegerField(null=True, blank=True, default=0)
    otp_time = models.CharField(null=True, blank=True, default="", max_length=255)
    image = models.CharField(max_length=255, blank=True, default="", null=True)

    def __str__(self):
        return f'{self.role.role_name} - {self.email}'


class Categories(models.Model):
    c_id = models.AutoField(primary_key=True)
    c_name = models.CharField(unique=True, null=True, blank=True, default="", max_length=50)

    def __str__(self):
        return self.c_name
