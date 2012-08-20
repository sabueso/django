from kecomo.nucleo.models import *
from django.contrib import admin

"""
class Pais(models.Model):
class Provincia(models.Model):
class Poblacion(models.Model):
class TipoPlato(models.Model):
class Restaurant(models.Model):
class Plato(models.Model):
"""

admin.site.register(Pais)
admin.site.register(Provincia)
admin.site.register(Poblacion)
#admin.site.register(TipoPlato)
class RestaurantAdmin(admin.ModelAdmin):
	list_display=('id','nombre','direccion','poblacionasoc')
admin.site.register(Restaurant,RestaurantAdmin)

admin.site.register(Plato)

