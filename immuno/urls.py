from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'immuno.views.home', name='home'),
    # url(r'^immuno/', include('immuno.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     url(r'^admin/', include(admin.site.urls)),
     url(r'^samples/(\d+)/?$', 'samples.views.summary'),
     url(r'^samples/(\d+)/clonotypes/?$', 'clonotypes.views.all'),
     url(r'^samples/(\d+)/pagination/?$', 'clonotypes.views.pagination'),
     url(r'^samples/', 'samples.views.home'),
)
