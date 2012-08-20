#!/usr/bin/env python
from celery.decorators import task
from guars.nucleo.models import *
#from django.shortcuts import render_to_response
#from django.http import HttpResponse, HttpResponseRedirect
#from time import sleep
#from operator import div

#@task
#def add(x, y):
#    return x + y

@task
def incremento(materiaid,cantidad):
        #datos=materias.objects.all().order_by('id')
	valoractual=Materiaporaldea.objects.get(id=materiaid)
	valoractual.nivelactual=valoractual.nivelactual+cantidad
	valoractual.enconstruccion=False
	valoractual.save()
	#return render_to_response('index.html',{'datos':datos})
	#return HttpResponseRedirect('/')

@task
def decremento(materiaid,cantidad):
        #datos=materias.objects.all().order_by('id')
        valoractual=Materiaporaldea.objects.get(id=materiaid)
        valoractual.nivelactual=valoractual.nivelactual-cantidad
        valoractual.save()
        #return render_to_response('index.html',{'datos':datos})
        #return HttpResponseRedirect('/')

@task
def actualizacion():
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
                try:
			incrementoob=Tempomateriapornivel.objects.get(materiaasoc=materia,nivel=nivelmat)
		except Tempomateriapornivel.DoesNotExist:
			break
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
		
	

