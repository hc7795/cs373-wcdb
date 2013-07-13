from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template
from wcdb import views
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'crisis.views.home', name='home'),
    # url(r'^crisis/', include('crisis.foo.urls')),
    
    url(r'^$', views.index, name='index'),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'CRI_IRAQWR', views.CRI_IRAQWR, name='CRI_IRAQWR'),
    url(r'CRI_HURIKE', views.CRI_HURIKE, name='CRI_HURIKE'),
    url(r'CRI_BAGAIR', views.CRI_BAGAIR, name='CRI_BAGAIR'),
    url(r'ORG_WHLORG', views.ORG_WHLORG, name='ORG_WHLORG'),
    url(r'ORG_REDCRS', views.ORG_REDCRS, name='ORG_REDCRS'),
    url(r'ORG_IAVETA', views.ORG_IAVETA, name='ORG_IAVETA'),
    url(r'PER_SADHUS', views.PER_SADHUS, name='PER_SADHUS'),
    url(r'PER_BUSDAD', views.PER_BUSDAD, name='PER_BUSDAD'),
    url(r'PER_BRAMAN', views.PER_BRAMAN, name='PER_BRAMAN'),

    (r'^crisis/$', 'wcdb.views.CrisesAll'),


    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
