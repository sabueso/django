# Create your views here.
from guars.nucleo.models import *
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
#logins
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
#peticiones
from django.template import Context, loader, RequestContext
#tareas
from guars.tareas import incremento
#import pytz
import time

from datetime import datetime
#Funcion de registro , genera estampas de todas las acciones importantes :)
def Huella(usuario,operacion,tipoacc,fecha,ipnavegador):
        Logeos.objects.create(user=usuario,accion=""+operacion+"",tipo=""+tipoacc+"",fecha=""+fecha+"",ip=ipnavegador)

#Changelog de lo que voy haciendo en el juego...
def changelog(request):
	cambios=Logeosdecambios.objects.all().order_by('-id')
	return render_to_response('changelog.html',{'cambios':cambios})

#1
def index(request):
        if request.user.is_authenticated():
	        aldea=Aldeaporusuario.objects.get(usuario=request.user.id,nombre="Aldea Principal")
		return HttpResponseRedirect('/aldea/'+str(aldea.id)+'')
	else:
		return render_to_response('index.html',context_instance=RequestContext(request))
#2
@login_required
def aldea(request,aldeaid):
        ipacceso=request.META.get('REMOTE_ADDR')
        ###########
	#barrasuperior de conteo de materias
        #aldea=Aldeaporusuario.objects.get(usuario=request.user.id,nombre="Aldea Principal")
        aldea=Aldeaporusuario.objects.get(id=aldeaid,usuario=request.user.id)
	incrementohuerto=incrementobosque=incrementomina=incrementobarrizal=0
	z=y=x=w=0
        listahuerto=PosicionMateria.objects.filter(materiaoriginal=Materiabase.objects.get(nombre="Huerto")).values('id')
	huerto=Materiaporaldea.objects.filter(aldeapert=aldea.id,materiapert__in=listahuerto).order_by('id')
	for i in huerto:
		materia=Materiaporaldea.objects.get(id=i.id)
		z=Tempomateriapornivel.objects.get(materiaasoc=materia.materiapert.materiaoriginal.id,nivel=i.nivelactual).incremento
		incrementohuerto=incrementohuerto+int(z)
        listabosque=PosicionMateria.objects.filter(materiaoriginal=Materiabase.objects.get(nombre="Bosque")).values('id')
        bosque=Materiaporaldea.objects.filter(aldeapert=aldea.id,materiapert__in=listabosque).order_by('id')
        for j in bosque:
                materia=Materiaporaldea.objects.get(id=j.id)
                y=Tempomateriapornivel.objects.get(materiaasoc=materia.materiapert.materiaoriginal.id,nivel=j.nivelactual).incremento
                incrementobosque=incrementobosque+int(y)
        listamina=PosicionMateria.objects.filter(materiaoriginal=Materiabase.objects.get(nombre="Mina")).values('id')
        mina=Materiaporaldea.objects.filter(aldeapert=aldea.id,materiapert__in=listamina).order_by('id')
        for k in mina:
                materia=Materiaporaldea.objects.get(id=k.id)
                x=Tempomateriapornivel.objects.get(materiaasoc=materia.materiapert.materiaoriginal.id,nivel=k.nivelactual).incremento
                incrementomina=incrementomina+int(x)
        listabarrizal=PosicionMateria.objects.filter(materiaoriginal=Materiabase.objects.get(nombre="Barrizal")).values('id')
        barrizal=Materiaporaldea.objects.filter(aldeapert=aldea.id,materiapert__in=listabarrizal).order_by('id')
        for m in barrizal:
                materia=Materiaporaldea.objects.get(id=m.id)
                w=Tempomateriapornivel.objects.get(materiaasoc=materia.materiapert.materiaoriginal.id,nivel=m.nivelactual).incremento
                incrementobarrizal=incrementobarrizal+int(w)
	###########
	listaaldeas=Aldeaporusuario.objects.filter(usuario=request.user.id)
	#logeo
	Huella(User.objects.get(pk=request.user.id),"visualizacion aldea "+request.user.username+"",'V',str(datetime.now()),ipacceso)
	return render_to_response('home.html',{'aldea':aldea,\
	'bosque':bosque,\
	'listaaldeas':listaaldeas,\
        'incrementohuerto':incrementohuerto,\
        'incrementobosque':incrementobosque,\
        'incrementomina':incrementomina,\
        'incrementobarrizal':incrementobarrizal,\
	'trigo':huerto,\
	'madera':bosque, 
	'arcilla':barrizal,\
	'metal':mina})

#mi banco de pruebas
#def materia(request):
#	datos=materias.objects.all().order_by('id')
#       madera=materias.objects.filter(nombre__icontains="madera").order_by('id')
#       trigo=materias.objects.filter(nombre__icontains='trigo').order_by('id')
#       metal=materias.objects.filter(nombre__icontains='metal').order_by('id')
#       arcilla=materias.objects.filter(nombre__icontains='arcilla').order_by('id')
#	return render_to_response('materias.html',{'madera':madera,'trigo':trigo,'metal':metal,'arcilla':arcilla})

def descmateria(request,aldeaid,materid):
	actualizable=""
	construyendo=""
        ipacceso=request.META.get('REMOTE_ADDR')
        ###########
        #barrasuperior de conteo de materias
        #aldea=Aldeaporusuario.objects.get(usuario=request.user.id,nombre="Aldea Principal")
        aldea=Aldeaporusuario.objects.get(id=aldeaid,usuario=request.user.id)
        incrementohuerto=incrementobosque=incrementomina=incrementobarrizal=0
        z=y=x=w=0
        listahuerto=PosicionMateria.objects.filter(materiaoriginal=Materiabase.objects.get(nombre="Huerto")).values('id')
        huerto=Materiaporaldea.objects.filter(aldeapert=aldea.id,materiapert__in=listahuerto).order_by('id')
        for i in huerto:
                materia=Materiaporaldea.objects.get(id=i.id)
                z=Tempomateriapornivel.objects.get(materiaasoc=materia.materiapert.materiaoriginal.id,nivel=i.nivelactual).incremento
                incrementohuerto=incrementohuerto+int(z)
        listabosque=PosicionMateria.objects.filter(materiaoriginal=Materiabase.objects.get(nombre="Bosque")).values('id')
        bosque=Materiaporaldea.objects.filter(aldeapert=aldea.id,materiapert__in=listabosque).order_by('id')
        for j in bosque:
                materia=Materiaporaldea.objects.get(id=j.id)
                y=Tempomateriapornivel.objects.get(materiaasoc=materia.materiapert.materiaoriginal.id,nivel=j.nivelactual).incremento
                incrementobosque=incrementobosque+int(y)
        listamina=PosicionMateria.objects.filter(materiaoriginal=Materiabase.objects.get(nombre="Mina")).values('id')
        mina=Materiaporaldea.objects.filter(aldeapert=aldea.id,materiapert__in=listamina).order_by('id')
        for k in mina:
                materia=Materiaporaldea.objects.get(id=k.id)
                x=Tempomateriapornivel.objects.get(materiaasoc=materia.materiapert.materiaoriginal.id,nivel=k.nivelactual).incremento
                incrementomina=incrementomina+int(x)
        listabarrizal=PosicionMateria.objects.filter(materiaoriginal=Materiabase.objects.get(nombre="Barrizal")).values('id')
        barrizal=Materiaporaldea.objects.filter(aldeapert=aldea.id,materiapert__in=listabarrizal).order_by('id')
        for m in barrizal:
                materia=Materiaporaldea.objects.get(id=m.id)
                w=Tempomateriapornivel.objects.get(materiaasoc=materia.materiapert.materiaoriginal.id,nivel=m.nivelactual).incremento
                incrementobarrizal=incrementobarrizal+int(w)
        ###########
	#estado de las materias 
	#
	materia=Materiaporaldea.objects.get(id=materid)
	proximonivel=int(materia.nivelactual) + 1
	matriztempomateriaactual=Tempomateriapornivel.objects.get(materiaasoc=materia.materiapert.materiaoriginal.id,nivel=materia.nivelactual)
        matriztempomateria=Tempomateriapornivel.objects.get(materiaasoc=materia.materiapert.materiaoriginal.id,nivel=proximonivel)
	tiempocrecimiento=time.strftime('%H:%M:%S', time.gmtime(matriztempomateria.tempo))
	if materia.enconstruccion == True:
		construyendo = "si"
	else:
		construyendo = "no"
        if aldea.depositohuerto < matriztempomateria.costehuerto or aldea.depositobosque < matriztempomateria.costebosque or aldea.depositomina < matriztempomateria.costemina or aldea.depositobarrizal < matriztempomateria.costebarrizal:
		actualizable="no"
	else:
		actualizable="si"
	Huella(User.objects.get(pk=request.user.id),"visualizacion materia "+materid+"de"+request.user.username+"","V",str(datetime.now()),ipacceso)
	return render_to_response('descmat.html',{'materia':materia,\
					'proximonivel':proximonivel,\
					'aldea':aldea,\
				        'incrementohuerto':incrementohuerto,\
				        'incrementobosque':incrementobosque,\
				        'incrementomina':incrementomina,\
					'incrementobarrizal':incrementobarrizal,\
				        'trigo':huerto,\
				        'madera':bosque,
				        'arcilla':barrizal,\
				        'metal':mina,\
					'actualizable':actualizable,\
					'tiempocrecimiento':tiempocrecimiento,\
					'construyendo':construyendo,\
					'matriztempomateriaactual':matriztempomateriaactual,\
					'matriztempomateria':matriztempomateria})

def subirnivel(request,aldeaid,mid):
        ipacceso=request.META.get('REMOTE_ADDR')
	materia=Materiaporaldea.objects.get(id=mid)
	matriztempomateria=Tempomateriapornivel.objects.get(materiaasoc=materia.materiapert.materiaoriginal.id,nivel=(int(materia.nivelactual)+int(1)))
        aldea=Aldeaporusuario.objects.get(id=aldeaid,usuario=request.user.id)
	if aldea.depositohuerto >= matriztempomateria.costehuerto and aldea.depositobosque >= matriztempomateria.costebosque and aldea.depositomina >= matriztempomateria.costemina and aldea.depositobarrizal >= matriztempomateria.costebarrizal and materia.enconstruccion == False:
		aldea.depositohuerto = aldea.depositohuerto - matriztempomateria.costehuerto
		aldea.depositobosque = aldea.depositobosque- matriztempomateria.costebosque
		aldea.depositomina = aldea.depositomina - matriztempomateria.costemina
		aldea.depositobarrizal =aldea.depositobarrizal - matriztempomateria.costebarrizal
		aldea.save()
		materia.enconstruccion='True'
                materia.save()
		resultado=incremento.apply_async(args=[mid,1],countdown=matriztempomateria.tempo)
	else:
	        return HttpResponse("<center>Eres un <b>listapio</b>!! Intentando hacer crecer materias por lo bajini? <b>CATCHED AND LOGGED!</b></center>")
	Huella(User.objects.get(pk=request.user.id),"subir nivel de "+mid+" para "+request.user.username+"","E",str(datetime.now()),ipacceso)
	return HttpResponseRedirect('/aldea/'+str(aldea.id)+'')


def listaedificios(request):
        return render_to_response('listaedificios.html')

def desloguearse(request):
	logout(request)
	return HttpResponseRedirect('/')

def actualizacion(request):
	consulta=Materiaporaldea.objects.all()
	for i in consulta:
		nivelmat=''
		materia=''
		incremento=''
		valoractual=''
		aldeaactual=''
		actualizar=''
		nivelmat=i.nivelactual
		aldeaactual=i.aldeapert.id
		materiatex=i.materiapert.materiaoriginal.get_tipo_display()
		materia=i.materiapert.materiaoriginal.id
		incrementoob=Tempomateriapornivel.objects.get(materiaasoc=materia,nivel=nivelmat)
		valoractual=Aldeaporusuario.objects.get(id=aldeaactual)
		if materiatex=="Huerto":
			actualizar=int(valoractual.depositohuerto)+int(incrementoob.incremento)
			valoractual.depositohuerto=actualizar
		elif materiatex=="Barrizal":
			actualizar=int(valoractual.depositobarrizal)+int(incrementoob.incremento)
			valoractual.depositobarrizal=actualizar
                elif materiatex=="Mina":
                        actualizar=int(valoractual.depositomina)+int(incrementoob.incremento)
                        valoractual.depositomina=actualizar
                elif materiatex=="Bosque":
                        actualizar=int(valoractual.depositobosque)+int(incrementoob.incremento)
                        valoractual.depositobosque=actualizar	
		valoractual.save()
	return HttpResponse("Ok , actualizados!")


def alta(request):
        if request.method == 'POST':
                form=FormularioAlta(request.POST)
                if form.is_valid():
                        usuario = form.cleaned_data['nombredeusuario']
                        pass1 = form.cleaned_data['pass1']
                        pass2 = form.cleaned_data['pass2']
                        correo = form.cleaned_data['correo']
			tipopersonaje = form.cleaned_data['personaje']
			#Creamos el registro para la tabla de usuarios
                        user = User.objects.create_user( ''+usuario+'',''+correo+'',''+pass1+'' )
                        perf = Perfil(user=user,baneado=False,personaje=tipopersonaje)
                        perf.save()
			nuevaldea=Aldeaporusuario(usuario=user,nombre="Aldea Principal",nivel=1,depositohuerto=0,depositobosque=0,depositomina=0,depositobarrizal=0)
			nuevaldea.save()
			listahuerto=PosicionMateria.objects.filter(materiaoriginal=Materiabase.objects.get(nombre="Huerto"))
			for i in listahuerto:
				creacionhuerto=Materiaporaldea(aldeapert=nuevaldea,materiapert=i,nivelactual=0)
				creacionhuerto.save()
			listabosque=PosicionMateria.objects.filter(materiaoriginal=Materiabase.objects.get(nombre="Bosque"))
			for n in listabosque:
				creacionbosque=Materiaporaldea(aldeapert=nuevaldea,materiapert=n,nivelactual=0)
				creacionbosque.save()
		        listamina=PosicionMateria.objects.filter(materiaoriginal=Materiabase.objects.get(nombre="Mina"))
			for j in listamina:
				creacionmina=Materiaporaldea(aldeapert=nuevaldea,materiapert=j,nivelactual=0)
				creacionmina.save()
			listabarrizal=PosicionMateria.objects.filter(materiaoriginal=Materiabase.objects.get(nombre="Barrizal"))
			for k in listabarrizal:
				creacionbarrizal=Materiaporaldea(aldeapert=nuevaldea,materiapert=k,nivelactual=0)
				creacionbarrizal.save()
                        return HttpResponse('Usuario creado...')
		else:
                        return HttpResponse('El formulario no es valido')
        else:
                form=FormularioAlta()
        return render_to_response('alta.html',{'form':form},context_instance=RequestContext(request))
