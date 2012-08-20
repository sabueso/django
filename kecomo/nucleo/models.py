from django.db import models
from django import forms
from django.forms import ModelForm, Textarea

#####
# Create your models here.
####
class Pais(models.Model):
	nombre=models.CharField(max_length=100)
	def __unicode__(self):
		return self.nombre

class Provincia(models.Model):
	pais=models.ForeignKey(Pais,related_name="Paisasoc")
	nombre=models.CharField(max_length=50)
	def __unicode__(self):
		#return "%s %s" % (self.nombre,self.id)
		return self.nombre

class Poblacion(models.Model):
	provincia=models.ForeignKey(Provincia,related_name="Provinciaasoc")
	nombre=models.CharField(max_length=50)
	def __unicode__(self):
		return "%s" % (self.nombre)

#class TipoPlato(models.Model):
#	nombre=models.CharField(max_length=30)
#	def __unicode__(self):
#		return self.nombre

class Restaurant(models.Model):
	nombre=models.CharField(max_length=150)
	direccion=models.CharField(max_length=150)
	poblacionasoc=models.ForeignKey(Poblacion,related_name="Poblacionasociada",null=True,blank=True)
	fechalta=models.DateTimeField('Fecha de creacion',null=True,blank=True)
	correoe=models.EmailField(max_length=80,null=True,blank=True)
	lon=models.IntegerField(max_length=6,null=True,blank=True)
	lat=models.IntegerField(max_length=6,null=True,blank=True)
	telefono=models.CharField(max_length=30,null=True,blank=True)
	descripcion=models.CharField(max_length=500,null=True,blank=True)
	votos=models.IntegerField(max_length=20,null=True,blank=True)
	cantvotos=models.IntegerField(max_length=20,null=True,blank=True)
	enlacegooglemaps=models.CharField(max_length=700,null=True,blank=True)
	def __unicode__(self):
		return self.nombre

class RestauranteForm(forms.ModelForm):
        class Meta:
		model = Restaurant
                fields = ['nombre','direccion','poblacionasoc','correoe','lon','lat','telefono','enlacegooglemaps']

class Plato(models.Model):
	hashtag=models.CharField(max_length=50)
	puntaje=models.IntegerField(max_length=20)
	comentario=models.CharField(max_length=50)
	tipoplato=models.CharField(max_length=50)
	restaurante=models.ForeignKey(Restaurant,related_name="Restauranteasoc")
	#tipo=models.ForeignKey(TipoPlato,related_name="Plato asociado")
	ip=models.IPAddressField()
	fecha=models.DateTimeField("Fecha de alta")
	navegador=models.CharField(max_length=200)
	def __unicode__(self):
		return self.hashtag

class VotarForm(forms.Form):
	mensaje = forms.CharField(max_length=180,widget=forms.TextInput)

class BusquedaForm(forms.Form):
	cajabusqueda = forms.CharField(max_length=50,widget=forms.TextInput)

class Registro(models.Model):
        fecha = models.DateTimeField('Fecha')
	accion=models.CharField(max_length=400)
	ip=models.IPAddressField()
	def __unicode__(self):
		return u'%s - %s - %s' % (self.fecha, self.accion, self.ip)

