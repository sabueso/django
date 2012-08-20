from w4rsforo.foro.models import *
from django.contrib import admin
from django.contrib.auth.models import User

class JuegoAdmin(admin.ModelAdmin):
	list_display=('id','nombre','descripcion','site')
admin.site.register(Juego,JuegoAdmin)


class ForoAdmin(admin.ModelAdmin):
	list_display=('id','fecha','titulo','descripcion','usuario','juego')
admin.site.register(Foro,ForoAdmin)

class SubforoAdmin(admin.ModelAdmin):
	list_display=('id','fecha','foroprincipal','titulo','descripcion','usuario')
admin.site.register(Subforo,SubforoAdmin)

class HiloAdmin(admin.ModelAdmin):
        def Cuerpo (self,obj):
        	if  len(obj.cuerpo) < 30:
        		return obj.cuerpo
		else:
        		return obj.cuerpo[:25]+'...'
	list_display=('id','fecha','subfororel','titulo','Cuerpo','usuario','abierto')
admin.site.register(Hilo,HiloAdmin)


class EntradasAdmin(admin.ModelAdmin):
        def Cuerpo (self,obj):
                if  len(obj.cuerpo) < 30:
                        return obj.cuerpo
                else:
                        return obj.cuerpo[:25]+'...'
	list_display=('id','fecha','hilopadre','Cuerpo','usuario')
admin.site.register(Entradas,EntradasAdmin)
