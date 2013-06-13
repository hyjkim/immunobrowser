from django.db import models
from patients.models import Patient

# Create your models here.


class Sample(models.Model):
    ''' Stores samples information. Multiple samples may belong to a patient.
    Each sample can have multiple clonotypes
    '''
    patient = models.ForeignKey(Patient)
    cell_type = models.CharField(max_length=100)
    draw_date = models.DateField(blank=True, null=True)

    def __unicode__(self):
        return u'%s %s %s' % (self.patient.name, self.draw_date, self.cell_type)
