from django.db import models

# Create your models here.
class Patient(models.Model):
  name = models.CharField(max_length=100)
  gender = models.CharField(max_length=1)
  disease = models.CharField(max_length=100)
  birthday = models.DateField(blank=True, null=True)

  def __unicode__(self):
    return self.name
