# These are general factories that are used for unittesting.
# Code for mocking out the django call stacks were made by Chase Seibert and
# are based on the source at
# http://chase-seibert.github.com/blog/2012/07/27/faster-django-view-unit-tests-with-mocks.html

import factory
#from mock import patch
from django.http import HttpRequest
from django.contrib.auth.models import User
#from django.http import Http404
from django.template import RequestContext


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
        request.POST = kwargs.get('GET', {})

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
    request = args[0]
    context = args[2]
    context['template'] = args[1]
    return context


