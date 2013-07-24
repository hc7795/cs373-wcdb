from django.conf.urls.defaults import patterns, include, url
# from django.views.generic.simple import direct_to_template
from django.contrib import admin
from wcdb import views
admin.autodiscover()

urlpatterns = patterns('',
	# Index page.
	url(r'^$', views.index, name='index'),
	url(r'index', views.index, name='index'),

	# Category pages.
	url(r'crises', views.crises, name='crises'),
	url(r'people', views.people, name='people'),
	url(r'organizations', views.organizations, name='organizations'),
	url(r'about', views.about, name='about'),
	# url(r'person', views.person, name='person'),
	

    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    (r'^crisis/$', 'wcdb.views.CrisesAll'),
)
