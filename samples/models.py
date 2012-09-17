from django.db import models
from patients.models import Patient

# Create your models here.
class Sample(models.Model):
  patient = models.ForeignKey(Patient)
  draw_date = models.DateField(blank=True, null=True)
