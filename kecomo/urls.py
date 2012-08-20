from django.conf.urls.defaults import *
from kecomo.nucleo.views import *
from kecomo import settings
from django.contrib import admin

admin.autodiscover()
urlpatterns = patterns('',
(r'^admin/(.*)', admin.site.root),
(r'^$','kecomo.nucleo.views.index'),
(r'^log/$','kecomo.nucleo.views.log'),
(r'^alta/$','kecomo.nucleo.views.altarestaurante'),
(r'^listado/$','kecomo.nucleo.views.listado'),
(r'^detalle/(?P<idrest>\d+)$','kecomo.nucleo.views.detalle'),
(r'^votar/(?P<idrest>\d+)$','kecomo.nucleo.views.votar'),
(r'^(?P<prov>(\w|\s|\d|\(|\))+)/$','kecomo.nucleo.views.provincialst'),
(r'^(?P<prov>(\w|\s|\d|\(|\))+)/(?P<pobl>(\w|\s|\d|\(|\)|\')+)/$','kecomo.nucleo.views.provypoblacion'),)
