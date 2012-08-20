from django.db import models
from django.contrib.auth.models import User
from django import forms

############################Tablas de sistema#############################
#A traves de aqui conseguimos una estampa de las acciones
eventoslog=(
('A','alta'),
('V','visual'),
('L','login'),
('E','ejecucion')
)

class Logeos(models.Model):
        user=models.ForeignKey(User,unique=False)
        fecha = models.DateTimeField('Fecha')
        accion=models.CharField(max_length=400)
	tipo=models.CharField(max_length=2,choices=eventoslog)
        ip=models.IPAddressField()
        def __unicode__(self):
                return u'%s - %s - %s' % (self.user, self.fecha, self.accion)

#Tabla donde van a parar todas las mejoreas que se hacen en el juego
#con fines informativos
class Logeosdecambios(models.Model):
        fecha = models.DateTimeField('Fecha')
        asunto=models.CharField(max_length=40)
        descripcion=models.TextField(max_length=500,null=True,blank=True)
        def __unicode__(self):
                return u'%s - %s' % (self.id , self.asunto)

############################Tablas propias del juego#############################
razas = (
('H','Hombre'),
('E','Enano'),
('L','Elfo'),
('O','Orco')
)
class Raza(models.Model):
	#nombre=models.ForeignKey(User,unique=True)
	descripcion=models.TextField(max_length=500,blank=True,null=True)
        tipo=models.CharField(max_length=1, choices=razas)
        def __unicode__(self):
		return ''+str(self.get_tipo_display())+''


#extension de perfil del usuario
class Perfil(models.Model):
        user=models.ForeignKey(User,unique=True)
	baneado=models.BooleanField(default=False)
	personaje=models.ForeignKey(Raza,related_name="RazaAsociada")

#tabla acc
#las distintas aldeas de cada usuario , en primera 
#instancia crearemos una aldea base , y una vez creados los edificios necesarios
#podremos crear aldeas secundarias.

class Aldeaporusuario(models.Model):
	usuario=models.ForeignKey(User,related_name="PropietarioAldea")
	nombre=models.CharField(max_length=30)
	nivel=models.IntegerField(max_length=6,null=True,blank=True)
	depositohuerto=models.IntegerField(max_length=9,null=True,blank=True)
	depositobosque=models.IntegerField(max_length=9,null=True,blank=True)
	depositomina=models.IntegerField(max_length=9,null=True,blank=True)
	depositobarrizal=models.IntegerField(max_length=9,null=True,blank=True)
	def __unicode__(self):
		#return u''+str(self.id)+'->'+str(self.usuario)+'->'+str(self.nombre)+''
		return ''+str(self.usuario)+'->'+str(self.nombre)+'->Nivel:'+str(self.nivel)+''

	
#################################################################################
#huerto, bosque, mina y barrizal
posiblesmaterias = (
('H', 'Huerto'),
('B', 'Bosque'),
('M', 'Mina'),
('Z','Barrizal'))

class Materiabase(models.Model):
	nombre=models.CharField(max_length=20)
	tipo=models.CharField(max_length=1, choices=posiblesmaterias)
        descripcion=models.TextField(max_length=500,blank=True,null=True)
	imagendesc=models.CharField(max_length=25,blank=True,null=True)
	def __unicode__(self):
		return self.nombre

#tabla desc
class PosicionMateria(models.Model):
	nombre=models.CharField(max_length=20)
	materiaoriginal=models.ForeignKey(Materiabase,related_name="Materiabase")
	nivelminimo=models.IntegerField(max_length=2)
	#campo a eliminar , no va a aqui
	####nivel=models.IntegerField(max_length=3)
	#Definimos el tipo de material por una sola letra
	#tipo=models.CharField(max_length=1, choices=posiblesmaterias)
	#agujero que ocupara en el css , holepos_9
	posicionmapa=models.CharField(max_length=10,blank=True,null=True)
	#Descripcion de la materia que se mostrara en la pestana de detalle
	#descripcion=models.TextField(max_length=500,blank=True,null=True)
        def __unicode__(self):
		return self.nombre



class Edificiosbase(models.Model):
        nombre=models.CharField(max_length=20)
        #tipo=models.CharField(max_length=1, choices=posiblesmaterias)
        descripcion=models.TextField(max_length=500,blank=True,null=True)
        imagenpeq=models.CharField(max_length=25,blank=True,null=True)
	imagengra=models.CharField(max_length=25,blank=True,null=True)
        def __unicode__(self):
                return self.nombre

###################################################################################

#tabla acc
#aqui definimos el nivel de las materias de cada aldea , y lo vamos haciendo crecer
class Materiaporaldea(models.Model):
        aldeapert=models.ForeignKey(Aldeaporusuario,related_name="UsuarioPerteneciente")
        materiapert=models.ForeignKey(PosicionMateria,related_name="MateriaAsociadaEnMapa")
        nivelactual=models.IntegerField(max_length=2)
	enconstruccion=models.BooleanField(default=False)
        def __unicode__(self):
		return ''+str(self.id)+''


#tabla desc
#ahora , definimos el tiempo de cada materia en cada nivel
class Tempomateriapornivel(models.Model):
	materiaasoc=models.ForeignKey(Materiabase,related_name="MateriaBase")
	nivel=models.IntegerField(max_length=2)
	tempo=models.IntegerField(max_length=6)
	incremento=models.IntegerField(max_length=9)
#	costedenivel=models.IntegerField(max_length=9)
	costehuerto=models.IntegerField(max_length=9)
	costebosque=models.IntegerField(max_length=9)
	costemina=models.IntegerField(max_length=9)
	costebarrizal=models.IntegerField(max_length=9)
	consumocereal=models.IntegerField(max_length=9)
	def __unicode__(self):
                return ''+str(self.materiaasoc)+'->Nivel:'+str(self.nivel)+'->Tiempo:'+str(self.tempo)+''

class FormularioAlta(forms.Form):
        nombredeusuario=forms.CharField(max_length=30)
        pass1=forms.CharField(widget=forms.PasswordInput, max_length=100)
        pass2=forms.CharField(widget=forms.PasswordInput, max_length=100)
        correo=forms.CharField(max_length=50)
	personaje=forms.ModelChoiceField(queryset=Raza.objects.all().order_by('tipo'))
        def clean_nombredeusuario(self):
                nombredeusuario = self.cleaned_data.get('nombredeusuario', '')
                if not User.objects.filter(username=nombredeusuario):
                        return nombredeusuario
                raise forms.ValidationError("El usuario ya existe")
        def clean_pass2(self):
                password = self.cleaned_data.get('pass1', '')
                if password != self.cleaned_data.get('pass2', ''):
                        raise forms.ValidationError("Las claves no coinciden")
                return password

