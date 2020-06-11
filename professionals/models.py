from django.db import models
from backend_app.models import Categories


class Projects(models.Model):
    p_id = models.AutoField(primary_key=True)
    category = models.ForeignKey(Categories, on_delete=models.SET_NULL, null=True)
    p_name = models.CharField(default="", null=True, blank=True, max_length=255)
    description = models.CharField(default="", null=True, blank=True, max_length=255)
    photo = models.CharField(max_length=255, default="", null=True, blank=True)
    email = models.EmailField(max_length=255, default="", null=True, blank=True)
    name = models.CharField(max_length=255, default="", null=True, blank=True)
