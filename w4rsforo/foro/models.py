from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.forms import ModelForm, Textarea


# Create your models here.

class Juego(models.Model):
	nombre=models.CharField(max_length=50)
	descripcion=models.TextField(max_length=30)
	site=models.URLField(max_length=200)
	def __unicode__(self):
		return self.nombre

class Foro(models.Model):
	titulo=models.CharField(max_length=100)
	descripcion=models.TextField(max_length=30)
	juego=models.ForeignKey(Juego,related_name="JuegoRelacionado")
	fecha=models.DateTimeField('Fecha de creacion')
	usuario=models.ForeignKey(User,related_name="Creador Foro")
	def __unicode__(self):
		return u'Foro: [%s]' % (self.titulo)

class Subforo(models.Model):
	titulo=models.CharField(max_length=100)
	descripcion=models.TextField(max_length=30)
	foroprincipal=models.ForeignKey(Foro,related_name="Foro_padre")
	fecha=models.DateTimeField('Fecha de creacion')
	usuario=models.ForeignKey(User,related_name="Creador Subforo")
	def __unicode__(self):
		return u'Subforo: [%s]' % (self.titulo)

class Hilo(models.Model):
	titulo=models.CharField(max_length=100)
	fecha=models.DateTimeField('Fecha de creacion')
	subfororel=models.ForeignKey(Subforo,related_name="Foro_padre")
	usuario=models.ForeignKey(User,related_name="Creador Hilo")
	cuerpo=models.TextField(max_length=5000)
	abierto=models.BooleanField()
	def __unicode__(self):
		return u'Hilo: [%s]' % (self.titulo)

class HiloForm(ModelForm):
        class Meta:
	        model = Hilo
        	fields = ['titulo','cuerpo']

class Entradas(models.Model):
	hilopadre=models.ForeignKey(Hilo,related_name="Hilopadre")
	fecha=models.DateTimeField('Fecha de creacion')
	cuerpo=models.TextField(max_length=5000)
        usuario=models.ForeignKey(User,related_name="Creador Entrada")

class EntradasForm(ModelForm):
	class Meta:
		model = Entradas
		fields = ['cuerpo']
	        #widgets = { 'cuerpo': Textarea(attrs={'cols': 800, 'rows': 2000}),}

#class Registro(forms.Form):
#	usuario=forms.CharField(max_length=20)
#	password=forms.CharField(max_length=50)
