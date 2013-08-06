from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from wcdb import views

admin.autodiscover()


urlpatterns = patterns('',
	# Index page.
	url(r'^$', views.index, name='index'),
	url(r'^index', views.index, name='index'),

	# Category pages.
	url(r'^crises', views.crises, name='crises'),
	url(r'^people', views.people, name='people'),
	url(r'^organizations', views.organizations, name='organizations'),
	url(r'^about', views.about, name='about'),
	url(r'^search', views.search, name='search'),
	url(r'^import_export', views.import_export, name='import_export'),

	# Individual pages.
	url(r'^crisis/([a-z0-9-]+)', views.crisis),
	url(r'^person/([a-z0-9-]+)', views.person),
	url(r'^org/([a-z0-9-]+)', views.org),

	# File uploads.
	url(r'^file_upload', views.fileUpload),

    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
