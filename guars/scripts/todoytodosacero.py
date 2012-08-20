#!/usr/bin/env python
import parametros
from guars.nucleo.models import *

Aldeaporusuario.objects.all().update(depositohuerto=0,depositobarrizal=0,depositobosque=0,depositomina=0)
Materiaporaldea.objects.all().update(enconstruccion=False,nivelactual=0)
from celery import task
task.discard_all()
