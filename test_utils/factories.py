# These are general factories that are used for unittesting.
# Code for mocking out the django call stacks were made by Chase Seibert and
# are based on the source at
# http://chase-seibert.github.com/blog/2012/07/27/faster-django-view-unit-tests-with-mocks.html

import factory
#from mock import patch
from django.http import HttpRequest
from django.contrib.auth.models import User
#from django.http import Http404
#from django.template import RequestContext
from clonotypes.models import AminoAcid, Recombination, Clonotype, ClonoFilter
from patients.models import Patient
from samples.models import Sample
from cf_comparisons.models import Comparison


class FakeMessages:
    ''' mocks the Django message framework, makes it easier to get
    the messages out '''

    messages = []

    def add(self, level, message, extra_tags):
        self.messages.append(str(message))

    @property
    def pop(self):
        return self.messages.pop()


def FakeRequestFactory(*args, **kwargs):
    ''' FakeRequestFactory, FakeMessages and FakeRequestContext are good for
    mocking out django views; they are MUCH faster than the Django test client.
    '''

    user = UserFactory()
    if kwargs.get('authenticated'):
        user.is_authenticated = lambda: True

    request = HttpRequest()
    request.user = user
    request._messages = FakeMessages()
    request.session = kwargs.get('session', {})
    if kwargs.get('POST'):
        request.method = 'POST'
        request.POST = kwargs.get('POST')
    else:
        request.method = 'GET'
        request.GET = kwargs.get('GET', {})

    return request


class UserFactory(factory.Factory):
    ''' using the excellent factory_boy library '''
    FACTORY_FOR = User
    username = factory.Sequence(lambda i: 'username' + i)
    first_name = factory.Sequence(lambda n: "Agent " + n)
    last_name = 'Doe'
    email = factory.Sequence(lambda i: 'blogtest%s@example.com' % i)

    @classmethod
    def _prepare(cls, create, **kwargs):
        password = kwargs.pop('password', None)
        user = super(UserFactory, cls)._prepare(create, **kwargs)
        if password:
            user.set_password(password)
            if create:
                user.save()
        return user


def render_to_response_echo(*args, **kwargs):
    ''' mocked render_to_response that just returns what was passed in,
    also puts the template name into the results dict '''
    context = args[1]
    locals = context.dicts[0]
    locals.update(dict(template_name=args[0]))
    return locals


def render_echo(*args, **kwargs):
    ''' mocked render that just returns what was passed in,
    also puts the template name into the results dict '''
#    request = args[0]
    context = args[2]
    context['template'] = args[1]
    return context


class PatientFactory(factory.Factory):
    FACTORY_FOR = Patient
    name = 'test patient'
    birthday = '2011-11-11'
    disease = 'fake disease'
    gender = 'M'


class SampleFactory(factory.Factory):
    FACTORY_FOR = Sample
    patient = factory.SubFactory(PatientFactory)
    draw_date = '2012-12-12'
    cell_type = 'cd4+'


class AminoAcidFactory(factory.Factory):
    '''
    Creates an Amino Acid
    '''
    FACTORY_FOR = AminoAcid
    sequence = 'CASSLGPLAEKETQYF'


class RecombinationFactory(factory.Factory):
    '''
    Creates a recombination
    '''
    FACTORY_FOR = Recombination
    amino_acid = factory.SubFactory(AminoAcidFactory)
    nucleotide = 'GGACTCGGCCATGTATCTCTGTGCCAGCAGCTTAGGTCCCCTAGCTGAAAAAGAGACCCA'
    v_family_name = 7
    v_gene_name = '(undefined)'
    v_ties = 'TRBV7-9'
    d_gene_name = 'TRBD1-2'
    j_gene_name = 'TRBJ2-5'
    j_ties = ''
    v_deletion = 1
    d5_deletion = 4
    d3_deletion = 7
    j_deletion = 3
    n2_insertion = 5
    n1_insertion = 5
    sequence_status = 'Productive'
    v_index = 19
    n1_index = 45
    n2_index = 35
    d_index = 40
    j_index = 50
    cdr3_length = 42


class ClonotypeFactory(factory.Factory):
    FACTORY_FOR = Clonotype
    sample = factory.SubFactory(SampleFactory)
    sequence_id = 'C0FW0ACXX_1_Patient-15-D_1'
    container = 'UCSC-Kim-P01-01'
    normalized_frequency = 9.336458E-6
    normalized_copy = 2
    raw_frequency = 1.6548345E-5
    copy = 2
    recombination = factory.SubFactory(RecombinationFactory)


class ClonoFilterFactory(factory.Factory):
    FACTORY_FOR = ClonoFilter
    sample = factory.SubFactory(SampleFactory)


class ComparisonFactory(factory.Factory):
    FACTORY_FOR = Comparison
    @classmethod
    def _prepare(cls, create, **kwargs):
        comp = super(ComparisonFactory, cls)._prepare(create, **kwargs)
        comp.clonofilters = [
                ClonoFilterFactory().id,
                ClonoFilterFactory().id
                ]
        return comp


