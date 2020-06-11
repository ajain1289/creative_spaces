from django.db import models
import datetime


class Questionnaire(models.Model):
    q_id = models.AutoField(primary_key=True)
    question = models.CharField(max_length=255, blank=True, null=True, default="")
    p_email = models.EmailField(max_length=255, blank=True, null=True, default="")
    u_email = models.EmailField(max_length=255, blank=True, null=True, default="")
    answer = models.CharField(max_length=255, blank=True, null=True, default="")
    status = models.NullBooleanField(default=0)


class Reviews(models.Model):
    review_id = models.AutoField(primary_key=True)
    rating = models.DecimalField(null=True, blank=True, max_digits=2, decimal_places=1, default=1.0)
    submission_date = models.DateField(null=True, blank=True, auto_now_add=datetime.date.today())
    p_email = models.EmailField(null=True, blank=True, default="", max_length=255)
    u_email = models.EmailField(null=True, blank=True, default="", max_length=255)
    review = models.CharField(null=True, blank=True, default="", max_length=255)
    #project

"""
from django.db.models import Q
obj = model-name.objects.filter(Q(p_email=request.user.email) | Q{status=0))
"""