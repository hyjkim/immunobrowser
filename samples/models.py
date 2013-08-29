from django.db import models
from patients.models import Patient
from django.contrib.auth.models import User
from django.db.models.query import QuerySet

# Create your models here.

class SampleQuerySet(QuerySet):
    ''' Custom queryset adds ability to
    search for private and public samples
    '''
    def public(self):
        '''
        Returns only samples that are not private
        '''
        return self.filter(private=False)

    def private(self, user):
        '''
        Returns public and private samples accessible by
        a user
        '''
        from django.db.models import Q
        qgroup = Q(private=True, users__in=[user.id])
        qgroup |= Q(private=False)
        return self.filter(qgroup)

    def search(self, terms):
        '''
        Searches text field of sample or parent and for matching text
        and returns all possible samples
        '''
        from django.db.models import Q
        import operator
        qgroup = reduce(operator.or_,
                [Q(Q(**{'cell_type__contains': term}) |
                    Q(**{'patient__name__contains': term}) |
                    Q(**{'patient__disease__contains': term})
                    ) for term in terms])
        return self.filter(qgroup)

class SampleManager(models.Manager):
    '''
    Replaces default manager to utilize a custom sample queryset
    '''
    def get_query_set(self):
        return SampleQuerySet(self.model)
    def __getattr__(self, attr, *args):
        if attr.startswith("_"): # or at least "__"
            raise AttributeError
        return getattr(self.get_query_set(), attr, *args)

class Sample(models.Model):
    ''' Stores samples information. Multiple samples may belong to a patient.
    Each sample can have multiple clonotypes
    '''
    patient = models.ForeignKey(Patient)
    cell_type = models.CharField(max_length=100)
    draw_date = models.DateField(blank=True, null=True)
    private = models.BooleanField(default=True)
    users = models.ManyToManyField(User)

    objects = SampleManager()


    def __unicode__(self):
        return u'%s %s %s' % (self.patient.name, self.draw_date, self.cell_type)
