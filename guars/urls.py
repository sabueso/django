from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^guars/', include('guars.foo.urls')),
###	#
    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
	(r'^admin/', include(admin.site.urls)),
	(r'^$','guars.nucleo.views.index'),
        (r'^alta/$','guars.nucleo.views.alta'),
	(r'^login','django.contrib.auth.views.login',{'template_name': 'login.html'}),
	(r'^desloguearse','guars.nucleo.views.desloguearse'),
	(r'^visordecambios','guars.nucleo.views.changelog'),
	(r'^logout/$','django.contrib.auth.views.logout'),
#	(r'^materia/','guars.nucleo.views.materia'),
	(r'edificios','guars.nucleo.views.listaedificios'),
        (r'^actualizacion/','guars.nucleo.views.actualizacion'),
	url(r'^aldea/(?P<aldeaid>\d+)$','guars.nucleo.views.aldea',name="aldea"),
	(r'^descmateria/(?P<aldeaid>\d+)/(?P<materid>\d+)','guars.nucleo.views.descmateria'),
	(r'^subirnivel/(?P<aldeaid>\d+)/(?P<mid>\d+)$','guars.nucleo.views.subirnivel'),
)
