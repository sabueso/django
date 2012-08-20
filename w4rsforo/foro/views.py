from django.template import Context, loader, RequestContext
from django.shortcuts import render_to_response
from w4rsforo.foro.models import *
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.contrib.auth import authenticate, login, logout
from django.forms import ModelForm
from django.forms.models import modelformset_factory
from django.forms.models import inlineformset_factory
from django.db.models import Max
import datetime

#variables para que no casque la funcion
#index al momento de compilar , aunque despues no sean
#usadas porque django tiene estas cosas ... se queda en los 
#bucles ...

#array de conteo de hilos
conteo=[]
#array de conteo de posts
conteop=[]
#array donde guardamos los id's de los ultimos hilos de cada foro
filtrohilo=[[],[]]
#ultimohilo=[]
sumatoriahilos=0
sumatoriaposts=0

def index(request):
	#Activamos debug , recordar que el fichero apunta a /tmp/foro.txt
        #import logging
        #logging.debug("%s",numerohilo)
	#conteo guarda la sumatoria de hilos en los foros
	conteo=[]
	#conteop guarda la sumatoria de posts	
	conteop=[]
	#contador temporal
	sumatoriahilos=0
	#contador temporal
	sumatoriaposts=0
	#conteo temporal de hilos seleccionados
	hilosnew=0
	#conteo temporal de entradas ...
	entradasnew=0
	#Consulta sql de hilos
	hilosd=""
	#Consulta sql de entradas
	entradasd=""
	#array que guarda los titulos de los ultimos hilos
	ultimohilot=[]
	#y este los usuarios ...
	ultimohilou=[]
	ultimohilof=[]
	filtrohilo=[]
	test=0
	#recuento de objetos devuelve foros (TOTAL)
	recuentodeobjetos = Foro.objects.filter().order_by('-fecha')
	#para cada objeto dentro de los foros , descargame los subforos...
	for a in recuentodeobjetos:
		filtrohilo=[]
		subforosd=Subforo.objects.filter(foroprincipal=int(a.id)).order_by('-fecha')
		#para cada objeto dentro de los subforos , decargame los hilos... y
		for b in subforosd:
			global filtrohilo
			filtrohilo.append(b.id)
			#logging.debug("%s array filtrohilo",filtrohilo)
			hilosd=Hilo.objects.filter(subfororel=b.id).order_by('-fecha')
			#cuenta lo hilos ...
			hilosnew=hilosd.count()
			#suma lo que has contado al valor anterior de sumatoriahilos
			sumatoriahilos=hilosnew+sumatoriahilos
			#para cada objeto dentro de los hilos , descargame las entradas...
			for c in hilosd:
				entradasd=Entradas.objects.filter(hilopadre=c.id)
				#cuenta las entradas
				entradasnew=entradasd.count()
				#sumalas al valor anterior
				sumatoriaposts=entradasnew+sumatoriaposts
			#ahora , una vez acabado el conteo de todos los posts de todos los hilos,hago un append que
			#equivale al valor de posts de cada foro
		#logging.debug("%s filtrohilo fuera del for",filtrohilo)
		maximohilo=Hilo.objects.filter(subfororel__in=filtrohilo).aggregate(Max('pk'))
		#logging.debug("%s valor de maximohilo",maximohilo)
		for n,m in maximohilo.iteritems():
			#logging.debug("%s m -> iteritems",m)
			if not m:
				consulta=[]
			else:
				consulta=Hilo.objects.get(pk=m)
				#consultahilomaximoi=consulta.pk
				#consultahilomaximot=consulta.titulo
				#consultahilomaximou=consulta.usuario.username
				#consultahilomaximof=consulta.fecha
			#logging.debug("%s ",consultahilomaximo)
			#if len(consultahilomaximot) < 15:
			#	ultimohilot[consultahilomaximoi]=''+consultahilomaximot+'|'+'',''+str(consultahilomaximof)+'',''+consultahilomaximou+''
			#else:
			#	ultimohilot[consultahilomaximoi]=''+consultahilomaximot[:15]+'...|'+'',''+str(consultahilomaximof)+'',''+consultahilomaximou+''
			ultimohilot.append(consulta)
			#ultimohilou.append(consultahilomaximou)
			#ultimohilof.append(consultahilomaximof)
		#logging.debug("%s",ultimohilot)
		conteop.append(sumatoriaposts)
		sumatoriaposts=0
		conteo.append(sumatoriahilos)
		sumatoriahilos=0
	#ultimohilo=str(ultimohilo)
	return render_to_response('foro/index.html',{'ultimohilot': ultimohilot,\
			#				'ultimohilou':ultimohilou,\
                        #                               'ultimohilof':ultimohilof,\
							'maximohilo': maximohilo,
							'recuentodeobjetos': recuentodeobjetos,\
							'conteo':conteo,\
							'conteop':conteop},\
							context_instance=RequestContext(request))

#Detalle de los 
def listasubforos(request,foronombre):
#	if not request.user.is_authenticated():
#		return HttpResponse("No tas logeado")
#	else:

		#import logging
		#logging.debug("%s",foronombre)					      
        	try:
			#iddelforo=Foro.objects.get(titulo=""+foronombre+"").id
			#listadodesubforos = Subforo.objects.filter(foroprincipal=int(iddelforo))
			# las lineas que estan comentadas aqui encima , son las que hacian
			# que la busqueda se hiciese por nombre , y no x ide de objeto
			# para simplificar la estructura de busqueda vamosa pasar todas las funciones
			# de busqueda a ID's o PK
			listadodesubforos = Subforo.objects.filter(foroprincipal=int(foronombre))
        	except Foro.DoesNotExist or Subforo.DoesNotExist:
			raise Http404
		return render_to_response('foro/subforos.html',{'subforo':listadodesubforos},context_instance=RequestContext(request))

def listahilos(request,foronombre,subforonombre):
#        if not request.user.is_authenticated():
#                return HttpResponse("No tas logeado")
#        else:
	        try:
	                #iddelsubforo = Subforo.objects.get(titulo=subforonombre).id
			#listadodehilos = Hilo.objects.filter(subfororel=int(iddelsubforo))	
			if request.user.is_authenticated():
				listadodehilos = Hilo.objects.filter(subfororel=int(subforonombre))
				formset=HiloForm()
                                if request.method == 'POST':
	                        	formset=HiloForm(request.POST)
                                        if formset.is_valid():
         	                               	test = formset.save(commit=False)
                                               	test.fecha=''+str(datetime.datetime.now())+''
                                               	#test.cuerpo='dedal-mola-mazo'
                                               	test.usuario=request.user
                                               	test.subfororel=Subforo.objects.get(pk=subforonombre)
						test.abierto=True
                                               	test.save()
                                               	formset=HiloForm()
					else:
                  	            		formset=HiloForm()

			else:
				listadodehilos = Hilo.objects.filter(subfororel=int(subforonombre))
				formset=EntradasForm()
			
	        except Subforo.DoesNotExist or Hilo.DoesNotExist:
	                raise Http404
	        return render_to_response('foro/hilos.html',{'hilo':listadodehilos,'formset':formset},context_instance=RequestContext(request))

def hilo(request,foronombre,subforonombre,numerohilo):
	#import logging
	#logging.debug("%s",numerohilo)
	#logging.debug("%s",subforonombre)
        #if not request.user.is_authenticated():
        #        return HttpResponse("No tas logeado")
        #else:
		##EntradasFormSet = modelformset_factory(Entradas)
		##formset = EntradasFormSet()
		try:	
			#iddelsubforo = Subforo.objects.get(titulo=subforonombre).id
			#hilobj=Hilo.objects.filter(pk=int(numerohilo),subfororel=iddelsubforo)
			#entradasobj=Entradas.objects.filter(hilopadre=int(numerohilo))
                        #iddelsubforo = Subforo.objects.get(titulo=subforonombre).id
			if request.user.is_authenticated():
	                        hilobj=Hilo.objects.filter(pk=int(numerohilo),subfororel=subforonombre).order_by('-fecha')
       		                entradasobj=Entradas.objects.filter(hilopadre=int(numerohilo)).order_by('fecha')
				hilo=Hilo.objects.get(id=numerohilo)
				if request.user.username == "esequenoexiste" :
	 				EntradasInlineFormset = inlineformset_factory(Hilo,Entradas,extra=0)
					if request.method == 'POST':
			       		        formset=EntradasInlineFormset(request.POST,instance=hilo)
				       	        if formset.is_valid():
                				        formset.save()
						else:
							formset=EntradasInlineFormset(instance=hilo)
				else:
					#usuarioinicial=int(request.user.id)
					##formulario = EntradasForm()
					##relleno=Entradas(usuario=User.objects.get(pk=usuarioinicial)
					formset=EntradasForm()
					if request.method == 'POST':
						formset=EntradasForm(request.POST)
						if formset.is_valid():
							test = formset.save(commit=False)
							test.fecha=''+str(datetime.datetime.now())+''
							#test.cuerpo='dedal-mola-mazo'
							test.usuario=request.user
							test.hilopadre=Hilo.objects.get(pk=numerohilo)
							test.save()
							formset=EntradasForm()
						else:
							formset=EntradasForm()
			else:
                                hilobj=Hilo.objects.filter(pk=int(numerohilo),subfororel=subforonombre)
                                entradasobj=Entradas.objects.filter(hilopadre=int(numerohilo))
                                hilo=Hilo.objects.get(id=numerohilo)
				formset=EntradasForm()
		except Hilo.DoesNotExist:
			raise Http404
		return render_to_response('foro/detallehilo.html',{'hiloenfoco':hilobj,'entradasfoco':entradasobj,'formset':formset},context_instance=RequestContext(request))

###################TEST DE COMENTARIOS####################
#def comentarios(request,foronombre,subforonombre,numerohilo):
#	hilo=Hilo.objects.get(id=numerohilo)
#	EntradasInlineFormset = inlineformset_factory(Hilo,Entradas,extra=1)
#	#formset=EntradasInlineFormset(instance=hilo)
#	if request.method == 'POST':
#		formset=EntradasInlineFormset(request.POST,instance=hilo)
#		if formset.is_valid():
#			formset.save()
#	else:
#		formset=EntradasInlineFormset(instance=hilo)
#		#if formset.is_valid():
#                #       formset.save()
#	return render_to_response("foro/comentarios.html",{'formset':formset,},context_instance=RequestContext(request))
##########################################################
def desloguearse(request):
	logout(request)
	return HttpResponseRedirect('/')

def registro(request):
        if request.user.is_authenticated():
                salida="Ya estas registrado logueado acutalmente como un usuario! Cabronazo!"
                return HttpResponse(salida)
	else:
		pass
	
	return render_to_response('registration/registro.html',context_instance=RequestContext(request))
