from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template
from django.contrib import admin
from wcdb import views
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),

	# Hardcoded HTML pages.
	url(r'CRI_IRAQWR', views.CRI_IRAQWR, name='CRI_IRAQWR'),
	url(r'CRI_HURIKE', views.CRI_HURIKE, name='CRI_HURIKE'),
	url(r'CRI_BAGAIR', views.CRI_BAGAIR, name='CRI_BAGAIR'),
	url(r'ORG_WHLORG', views.ORG_WHLORG, name='ORG_WHLORG'),
	url(r'ORG_REDCRS', views.ORG_REDCRS, name='ORG_REDCRS'),
	url(r'ORG_IAVETA', views.ORG_IAVETA, name='ORG_IAVETA'),
	url(r'PER_SADHUS', views.PER_SADHUS, name='PER_SADHUS'),
	url(r'PER_BUSDAD', views.PER_BUSDAD, name='PER_BUSDAD'),
	url(r'PER_BRAMAN', views.PER_BRAMAN, name='PER_BRAMAN'),

    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    (r'^crisis/$', 'wcdb.views.CrisesAll'),
)
