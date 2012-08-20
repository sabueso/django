# Create your views here.
from django.template import Context, loader, RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from kecomo.nucleo.models import *
from django.db.models import Q
from django.db.models import Avg
from django.forms import ModelForm
from django.forms.models import modelformset_factory
from django.forms.models import inlineformset_factory
from operator import itemgetter, attrgetter

import datetime,re

#funcion de escritura de logs
def Huella(operacion,fecha,ipnavegador):
        Registro.objects.create(accion=""+operacion+"",fecha=""+fecha+"",ip=ipnavegador)

#index de la web , actualmente nos permite buscar y ver los ultimos restaurantes agregados
def index(request):
	provincias=Provincia.objects.all()
	#poblaciones=Poblacion.objects.filter(Q(provincia=8)).order_by('nombre')
	poblaciones="-"
	ultimosrestaurantes=Restaurant.objects.all().order_by('-id')[:5]
        formulario=BusquedaForm()
        if request.method ==  'POST':
                formulario=BusquedaForm(request.POST)
                if formulario.is_valid():
                        textoabuscar = formulario.cleaned_data['cajabusqueda']
                        restresultados=Restaurant.objects.filter(nombre__icontains=''+textoabuscar+'')
                        if str(restresultados) == "[]":
                                salida="<center>No hay ningun Restaurant llamado "+textoabuscar+". Crealo <a href=\"http://www.kecomo.com/alta/\">tu mismo ahora!</a></center>"
                                return HttpResponse(salida)
                        else:
                                return render_to_response('resultbusquedapob.html',{'restresultados':restresultados})
	return render_to_response('index.html',{'provincias':provincias,'poblaciones':poblaciones,'ultimosrestaurantes':ultimosrestaurantes,'formulario':formulario})

#Funcion que se mostrar en /logs lo que esta sucediendo
def log(request):
        fechaactual=str(datetime.datetime.now())
        ipactual=request.META.get('REMOTE_ADDR')
	logs=Registro.objects.all().order_by('-fecha')[:25]
	bucle=[]
	for line in logs:
		bucle.append(''+str(line)+'<br />')
	Huella("Se ha enviado visitado el log desde la "+ipactual+"",fechaactual,ipactual)
	return HttpResponse(bucle)

#Aqui establecemos una provincia y sacamos el listado de las pobaciones
def provincialst(request,prov):
	try:
		provincias=Provincia.objects.get(Q(nombre=prov))
	except Provincia.DoesNotExist:
		salida="<center>La provincia <b>"+prov+"</b> buscas no existe...</center"
		return HttpResponse(salida)
	poblaciones=Poblacion.objects.filter(provincia=provincias).order_by('nombre')
        formulario=BusquedaForm()
        if request.method ==  'POST':
                formulario=BusquedaForm(request.POST)
                if formulario.is_valid():
                        textoabuscar = formulario.cleaned_data['cajabusqueda']
                        restresultados=Restaurant.objects.filter(nombre__icontains=''+textoabuscar+'').filter(poblacionasoc__in=poblaciones)
                        if str(restresultados) == "[]":
                                salida="<center>No hay ningun Restaurant llamado "+textoabuscar+". Crealo <a href=\"http://www.kecomo.com/alta/\">tu mismo ahora!</a></center>"
                                return HttpResponse(salida)
                        else:
				return render_to_response('resultadobusquedaprov.html',{'restresultados':restresultados})
	return render_to_response('provsel.html',{'provincias':provincias,'poblaciones':poblaciones,'formulario':formulario})
#Aqui ya tenemos provincia y poblacion, y ahora , podemos buscar tranquilos refinando la busqueda con la poblacion y 
#parte del nombre como datos.
def provypoblacion(request,prov,pobl):
        try:
                provincias=Provincia.objects.get(Q(nombre=prov))
        except Provincia.DoesNotExist:
                salida="<center>La provincia <b>"+prov+"</b> buscas no existe...</center"
                return HttpResponse(salida)
	try:
		poblaciones=Poblacion.objects.get(Q(nombre=pobl))
	except Poblacion.DoesNotExist:
		salida="<center>La poblacion <b>"+pobl+"</b> buscas no existe...</center"
		return HttpResponse(salida)
        formulario=BusquedaForm()
        if request.method ==  'POST':
                formulario=BusquedaForm(request.POST)
                if formulario.is_valid():
                        textoabuscar = formulario.cleaned_data['cajabusqueda']
			restresultados=Restaurant.objects.filter(nombre__icontains=''+textoabuscar+'').filter(poblacionasoc=poblaciones.id)
			if str(restresultados) == "[]":
				salida="<center>No hay ningun Restaurant llamado "+textoabuscar+". Crealo <a href=\"http://www.kecomo.com/alta/\">tu mismo ahora!</a></center>"
				return HttpResponse(salida)
			else:
				return render_to_response('resultbusqueda.html',{'restresultados':restresultados})
	return render_to_response('provselpob.html',{'provincias':provincias,'poblaciones':poblaciones,'formulario':formulario})

#De momento sin uso
def buscar(request,pobl):
        try:
        	poblaciones=Poblacion.objects.get(Q(nombre=pobl))
        except Poblacion.DoesNotExist:
                salida="<center>La poblacion <b>"+pobl+"</b> buscas no existe...</center"
                return HttpResponse(salida)
	formulario=BusquedaForm()
        if request.method ==  'POST':
	        formulario=BusquedaForm(request.POST)
        	if formulario.is_valid():
                	textoabuscar = formulario.cleaned_data['cajabusqueda']
			formulario=BusquedaForm()
	return HttpResponse(textoabuscar)

def altarestaurante(request):
	test=""
	formset=RestauranteForm()
        if request.method == 'POST':
        	formset=RestauranteForm(request.POST)
                if formset.is_valid():
                	formulario = formset.save(commit=False)
                        formulario.fechalta=''+str(datetime.datetime.now())+''
                        #test.usuario=request.user
                        #test.subfororel=Subforo.objects.get(pk=subforonombre)
                        #test.abierto=True
                        #test.save()
			formulario.save()
                        formset=RestauranteForm()
			return HttpResponseRedirect('/listado/') 
		else:
			formset=RestauranteForm()
	return render_to_response('altarest.html',{'formset':formset},context_instance=RequestContext(request))

#Apartado de informacion sobre el restaurante , con una previsualizacion de los platos que se estan votando ese dia
def detalle(request,idrest):
	try:
		relegido=Restaurant.objects.get(id=idrest)
	except Restaurant.DoesNotExist:
                salida="El Restaurante que intentas consulta , no existe!"
                return HttpResponse(salida)
	return render_to_response('detallerest.html',{'relegido':relegido})

#Apartado donde votar los platos , aqui esta la magia
def votar(request,idrest):
	fechaactual=str(datetime.datetime.now())
	ipactual=request.META.get('REMOTE_ADDR')
	navegadorcliente=request.META.get('HTTP_USER_AGENT')
	platosapromediar=[]
	#Clase de valores , solo etiquetamos aqui los grupos de datos del array
	class Valores:
        	def __init__(self, hashtag, promedio):
                	self.hashtag = hashtag
                	self.promedio = promedio
        	def __repr__(self):
                	return repr((self.hashtag, self.promedio))

        try:
	        relegido=Restaurant.objects.get(id=idrest)
		#Todos los platos
		consultadehoy=Plato.objects.filter(restaurante=relegido).filter(fecha__range=(''+str(datetime.date.today())+' 00:00:00',''+str(datetime.date.today())+' 23:59:59'))
		#Ordenados por id , para mostrar como ultimos platos agregados
		platos=consultadehoy.order_by('-id')[:10]
		#Agrupamos los platos
		distintos=consultadehoy.values('hashtag').distinct()
		#Ahora sacamos los promedios para los distintos platos
		for i in distintos:
			consulta=consultadehoy.filter(hashtag=str(i['hashtag'])).aggregate(Avg('puntaje'))
			platosapromediar.append(Valores(''+str(i['hashtag'])+'',consulta['puntaje__avg']))
		formulario=VotarForm()
		if request.method ==  'POST':
			formulario=VotarForm(request.POST)
			if formulario.is_valid():
				mensahashtag = formulario.cleaned_data['mensaje']
				#Aqui extraemos el hashtag
				if not re.search('^@\w+',mensahashtag) :
					return HttpResponse ("No hay Hashtag inicial!")
				else:
					hashtagfinal=re.search('^@\w+',mensahashtag)
				#Puntaje
				textomasnumero=re.search('^@\w+\s+\d+\s+',mensahashtag)
				try:
					puntajesconespacios=re.sub('^@\w+\s+','',textomasnumero.group(0))
                                except AttributeError:
                                        return HttpResponse("No existe puntaje o no es correcto!")
				puntajefinal=re.sub('\s','',puntajesconespacios)
				valores=['0','1','2','3','4','5','6','7','8','9','10']
				if puntajefinal not in valores:
					return HttpResponse('Has enviado "'+str(puntajefinal)+'" Los puntajes van de 0  a 10!!! o deben ser numeros enteros!')
				#puntajefinal=re.search('^@\w+\s')
				prueba=re.search(r'(?P<hashtag>^@\w+)(?P<espacio>\s{1})(?P<puntaje>\d+(?=\s{1}))(?P<comentario>.+)',mensahashtag)
				puntajefinal=prueba.group('puntaje')
				#Mensaje
				mensajedelfinal=prueba.group('comentario')
				Huella("Se ha enviado el hashtag->"+mensahashtag+"",fechaactual,ipactual)
				Plato.objects.create(hashtag=prueba.group('hashtag'),puntaje=prueba.group('puntaje'),comentario=prueba.group('comentario'),tipoplato='Plato',restaurante=relegido,ip=ipactual,fecha=fechaactual,navegador=navegadorcliente)
				return HttpResponse('<html><head><meta http-equiv="refresh" content="2; url=http://www.kecomo.com/votar/'+str(idrest)+'"></head> <body><center> Gracias por enviar <b>'+hashtagfinal.group(0)+'</b>, con puntaje <b>'+puntajefinal+'</b> con mensaje <b>\"'+mensajedelfinal+'\"</b></center></body></html>') # Redirect after POST
	except Restaurant.DoesNotExist:
		salida="El Restaurante que intentas consulta , no existe!"
        	return HttpResponse(salida)
	#Ahora , ordenamos los objetos x los que tienen mejor promedio
	platosapromediar=sorted(platosapromediar,key=attrgetter('promedio'),reverse=True)[:5]
	return render_to_response('votar.html',{'relegido':relegido,'formulario':formulario,'platos':platos,'distintos':distintos,'platosapromediar':platosapromediar})

#Listado de consulta , minimalista
def listado(request):
	consulta=Restaurant.objects.all().order_by('-id')
	return render_to_response('listado.html',{'consulta':consulta})
