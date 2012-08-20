#!/usr/bin/env python
import parametros
from guars.nucleo.models import *

#este script pone las materias de todas las aldeas a cero
#CUIDADO!

Aldeaporusuario.objects.all().update(depositohuerto=0,depositobarrizal=0,depositobosque=0,depositomina=0)
