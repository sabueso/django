from guars.nucleo.models import *
from django.contrib import admin


class PerfilAdmin(admin.ModelAdmin):
	list_display=('user','baneado','personaje')
admin.site.register(Perfil,PerfilAdmin)

admin.site.register(Raza)
class AldeaporusuarioAdmin(admin.ModelAdmin):
	list_display=('id','usuario','nombre','nivel','depositohuerto','depositobosque','depositomina','depositobarrizal')
admin.site.register(Aldeaporusuario,AldeaporusuarioAdmin)

class MateriabaseAdmin(admin.ModelAdmin):
	list_display=('id','nombre','tipo','descripcion','imagendesc')
admin.site.register(Materiabase,MateriabaseAdmin)


class EdificiosbaseAdmin(admin.ModelAdmin):
        list_display=('id','nombre','descripcion','imagenpeq','imagengra')
admin.site.register(Edificiosbase,EdificiosbaseAdmin)

class MateriaporaldeaAdmin(admin.ModelAdmin):
	list_display=('id','aldeapert','materiapert','nivelactual','enconstruccion')
admin.site.register(Materiaporaldea,MateriaporaldeaAdmin)

class TempomaterianivelAdmin(admin.ModelAdmin):
	#list_display=('id','materiaasoc','nivel','tempo','incremento','costedenivel')
	list_display=('materiaasoc',\
        'nivel',\
        'tempo',\
        'incremento',\
        'costehuerto',\
        'costebosque',\
        'costemina',\
        'costebarrizal',\
        'consumocereal')

admin.site.register(Tempomateriapornivel,TempomaterianivelAdmin)

class PosicionMateriaAdmin(admin.ModelAdmin):
	list_display=('id','nombre','materiaoriginal','nivelminimo','posicionmapa')
admin.site.register(PosicionMateria,PosicionMateriaAdmin)

class LogeosdecambiosAdmin(admin.ModelAdmin):
	list_display=('id','fecha','asunto','descripcion')
admin.site.register(Logeosdecambios,LogeosdecambiosAdmin)
