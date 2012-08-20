from django import forms
from django.db import models
from django.forms import ModelForm
from tinymce.widgets import TinyMCE
from tinymce import models as tinymce_models


# Create your models here.

class Categoria(models.Model):
	nombre=models.CharField(max_length=50)
        def __unicode__(self):
                return self.nombre

class Articulos(models.Model):
	fecha = models.DateTimeField('Fecha Alta')
	propietario=models.CharField(max_length=50)
	asunto=models.CharField(max_length=100)
	cuerpo=models.TextField(max_length=5000)
	def __unicode__(self):
		return self.asunto
#class VistaRica(models.Model):
#	prueba = tinymce_models.HTMLField()

#class ArticulosForm(ModelForm):
#        fecha = forms.DateTimeField('Fecha Baja!')
#        propietario=forms.CharField(max_length=50)
#        asunto=forms.CharField(max_length=100)
#	cuerpo = forms.CharField(widget=TinyMCE(attrs={'cols': 60, 'rows': 20}))
#	class Meta:
#		model = Articulos

#class Articulos(model.Model):

