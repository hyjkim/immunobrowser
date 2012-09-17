from django.db import models
from patients.models import Patient

# Create your models here.
class Sample(models.Model):
  patient = models.ForeignKey(Patient)
  cell_type = models.CharField(max_length=100)
  draw_date = models.DateField(blank=True, null=True)
  def __unicode__(self):
    return self.patient.name + " " + self.draw_date.isoformat() + " " + self.cell_type
