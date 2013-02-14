import urllib
from django.test import TestCase

def url_with_querystring(path, **kwargs):
    return path + '?' + urllib.urlencode(kwargs)


