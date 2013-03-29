from django.conf.urls import patterns, include, url
from django.conf import settings

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

                       # Dynamic
                       url(r'^amino_acid/(\d+)?$', 'clonotypes.views.amino_acid_detail'),
                       url(r'^clonofilter/(\d+)/domination.png', 'clonotypes.views.domination_graph'),
                       url(r'^clonofilter/(\d+)/functionality.png', 'clonotypes.views.functionality_graph'),
                       url(r'^clonofilter/(\d+)/j_usage.png', 'clonotypes.views.j_usage_graph'),
                       url(r'^clonofilter/(\d+)/v_usage.png', 'clonotypes.views.v_usage_graph'),
                       url(r'^samples/(\d+)/bubble.png', 'clonotypes.views.bubble_default'),
                       url(r'^samples/(\d+)/spectratype.png', 'clonotypes.views.spectratype_default'),
                       url(r'^samples/(\d+)/?$', 'samples.views.summary'),
                       url(r'^samples/(\d+)/clonotypes/?$',
                           'clonotypes.views.all'),
                       url(r'^clonotype/(\d+)$$', 'clonotypes.views.detail'),
                       url(r'^samples/', 'samples.views.home'),
                       url(r'^compare/(\d+)/bubble.png', 'cf_comparisons.views.bubble'),
                       url(r'^compare/(\d+)/spectratype.png', 'cf_comparisons.views.spectratype'),
                       url(r'^compare/(\d+)', 'cf_comparisons.views.compare'),
                       url(r'^compare/samples', 'cf_comparisons.views.sample_compare'),



                       # Media and static
                       url(r'^assets/(?P<path>.*)$', 'django.views.static.serve', { 'document_root' : settings.MEDIA_ROOT }),
                       )
