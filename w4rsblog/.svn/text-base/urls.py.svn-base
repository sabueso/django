from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	(r'^comments/', include('django.contrib.comments.urls')),
	(r'^$', 'w4rsblog.blog.views.index'),
	(r'^(?P<articulos_id>\d+)', 'w4rsblog.blog.views.detalle'),
	#Foro
	#(r'^foro/$', 'w4rs.foro.views.index'),
	#(r'^foro/login/$','django.contrib.auth.views.login',{'template_name': 'foro/login.html'}),
	#(r'^foro/desloguearse','w4rs.foro.views.desloguearse'),
	#(r'^foro/logout/$','django.contrib.auth.views.logout'),
	#(r'^foro/accounts/', include('registration.backends.default.urls')),
	#(r'^foro/(?P<foronombre>\w+)/$','w4rs.foro.views.listasubforos'),
	#(r'^foro/(?P<foronombre>\w.+)/(?P<subforonombre>\w.+)/$','w4rs.foro.views.listahilos'),
	#(r'^foro/(?P<foronombre>\w.+)/(?P<subforonombre>\w.+)/(?P<numerohilo>\d+)','w4rs.foro.views.hilo'),
	(r'^tinymce/', include('tinymce.urls')),
	(r'^admin/(.*)', admin.site.root),)
