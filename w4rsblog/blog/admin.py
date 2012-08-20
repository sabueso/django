from w4rsblog.blog.models import *
from django.contrib import admin
from django.contrib.auth.models import User


class CategoriaAdmin(admin.ModelAdmin):
	list_display=('id','nombre')
admin.site.register(Categoria,CategoriaAdmin)

class ArticulosAdmin(admin.ModelAdmin):
	def Cuerpo (self,obj):
             	if len(obj.cuerpo) < 25:
                       	return obj.cuerpo
              	else:
                       	return obj.cuerpo[:40]+'...'
	list_display=('id','fecha','propietario','asunto','Cuerpo')
       	fieldsets=[
               ('Cabecera de Articulo',  {'fields': [('fecha','asunto')]}),
                ('Cuerpo', {'fields': ['cuerpo']})
                ]
	def save_model(self, request, obj, form, change):
		obj.propietario=str(request.user)
		obj.save()
	class Media:
       		js = ('/media/js/tiny_mce/tiny_mce.js','/media/js/tiny_mce/textareas.js',)

admin.site.register(Articulos,ArticulosAdmin)
