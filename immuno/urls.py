from django.conf.urls import patterns, include, url
from django.conf import settings
from tastypie.api import Api
from immuno.api import PatientResource, SampleResource

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

# tastypie api setup
v1_api = Api(api_name='v1')
v1_api.register(PatientResource())
v1_api.register(SampleResource())

urlpatterns = patterns('',
                       # Uncomment the admin/doc line below to enable admin documentation:
                       # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

                       # Uncomment the next line to enable the admin:
                       url(r'^admin/', include(admin.site.urls)),
                       url('^accounts/', include('django.contrib.auth.urls')),

                       # Dynamic
                       url(r'^patients/(\d+)/$', 'patients.views.patient_summary'),

                       url(r'^dashboard$', 'dashboard.views.explorer'),
                       url(r'^dashboard/compare/(\d+)?$', 'dashboard.views.dashboard_comparison'),
                       url(r'^dashboard/menu.json$', 'dashboard.views.menu_json'),
                       url(r'^dashboard/add_samples$', 'dashboard.views.add_samples'),
                       url(r'^dashboard/add_samples_v2$', 'dashboard.views.add_samples_v2'),
                       url(r'^dashboard_v2/?(\d+)?$', 'dashboard.views.dashboard_v2'),
                       url(r'^dashboard/remove_clonofilter$', 'dashboard.views.remove_clonofilter'),
#                       url(r'^dashboard_v2', 'dashboard.views.dashboard_v2'),

                       url(r'^amino_acid/(\d+)?$', 'clonotypes.views.amino_acid_detail'),

                       url(r'^clonofilter/(\d+)/domination.png', 'clonotypes.views.domination_graph'),
                       url(r'^clonofilter/(\d+)/functionality.png', 'clonotypes.views.functionality_graph'),
                       url(r'^clonofilter/(\d+)/j_usage.png', 'clonotypes.views.j_usage_graph'),
                       url(r'^clonofilter/(\d+)/v_usage.png', 'clonotypes.views.v_usage_graph'),

                       url(r'^samples/$', 'samples.views.home'),
                       url(r'^samples/(\d+)/bubble.png', 'clonotypes.views.bubble_default'),
                       url(r'^samples/(\d+)/spectratype.png', 'clonotypes.views.spectratype_default'),
                       url(r'^samples/(\d+)/?$', 'samples.views.summary'),
                       url(r'^samples/(\d+)/clonotypes/?$',
                           'clonotypes.views.all'),

                       url(r'^clonotype/(\d+)$', 'clonotypes.views.detail'),

                       url(r'^compare/?(\d+)?/scatter_nav', 'cf_comparisons.views.scatter_nav'),
                       url(r'^compare/(\d+)?/shared_clones', 'cf_comparisons.views.shared_clones'),
                       url(r'^compare/(\d+)/bubble.png', 'cf_comparisons.views.bubble'),
                       url(r'^compare/(\d+)/spectratype.png', 'cf_comparisons.views.spectratype'),
                       url(r'^compare/(\d+)/filter_forms', 'cf_comparisons.views.filter_forms'),
                       url(r'^compare/(\d+)/d3_test', 'cf_comparisons.views.d3_test'),
                       url(r'^compare/(\d+)/update', 'cf_comparisons.views.update'),
                       url(r'^compare/(\d+)', 'cf_comparisons.views.compare'),
                       url(r'^compare/samples', 'cf_comparisons.views.sample_compare'),

                       # api
                        url(r'^api/', include(v1_api.urls)),


                       # Media and static
#                       url(r'^static/(?P<path>.*)$', 'django.views.static.serve', { 'document_root' : settings.MEDIA_ROOT }),

                       # testing
                       url(r'^qunit$', 'fts.views.qunit'),
                       )
