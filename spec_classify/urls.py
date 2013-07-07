from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^browse/$', 'browse.views.index'),
	url(r'^browse/fmenu/$', 'browse.views.fmenu'),
	url(r'^browse/obs_detail/$', 'browse.views.obs_detail'),
	url(r'^browse/wave_plot/$', 'browse.views.wave_plot'),
	url(r'^classify/$', 'classify.views.index'),
    # Examples:
    # url(r'^$', 'spec_classify.views.home', name='home'),
    # url(r'^spec_classify/', include('spec_classify.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
