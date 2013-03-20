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
from clonotypes.models import AminoAcid, Rearrangement, Clonotype
from patients.models import Patient
from samples.models import Sample


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
    username = factory.Sequence(lambda i: 'blogtest' + i)
    first_name = 'John'
    last_name = 'Doe'
    email = factory.Sequence(lambda i: 'blogtest%s@example.com' % i)


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


class RearrangementFactory(factory.Factory):
    '''
    Creates a rearrangement
    '''
    FACTORY_FOR = Rearrangement
    nucleotide = 'ATGCATGC'
    v_family_name = 'v1'
    v_gene_name = '1'
    v_ties = '1,2'
    d_gene_name = '2'
    j_gene_name = 'j3'
    j_ties = 'j4,j5'
    sequence_status = 'Productive'
    v_deletion = 2
    d5_deletion = 3
    d3_deletion = 2
    j_deletion = 3
    n2_insertion = 4
    n1_insertion = 5
    v_index = 3
    n1_index = 4
    n2_index = -1
    d_index = 10
    j_index = 5
    cdr3_length = 42


class AminoAcidFactory(factory.Factory):
    '''
    Creates an Amino Acid
    '''
    FACTORY_FOR = AminoAcid
    sequence = 'CASS'

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

class ClonotypeFactory(factory.Factory):
    FACTORY_FOR = Clonotype
    sample = factory.SubFactory(SampleFactory)
    sequence_id = 'C0FW0ACXX_1_Patient-15-D_1'
    container = 'UCSC-Kim-P01-01'
    nucleotide = 'GGACTCGGCCATGTATCTCTGTGCCAGCAGCTTAGGTCCCCTAGCTGAAAAAGAGACCCA'
    amino_acid = 'CASSLGPLAEKETQYF'
    normalized_frequency = 9.336458E-6
    normalized_copy = 2
    raw_frequency = 1.6548345E-5
    copy = 2
    cdr3_length = 42
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
