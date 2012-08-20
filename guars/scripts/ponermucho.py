#!/usr/bin/env python
import parametros
from guars.nucleo.models import *

#este script pone las materias de todas las aldeas a cero
#CUIDADO!

Aldeaporusuario.objects.all().update(depositohuerto=999990,depositobarrizal=99990,depositobosque=99990,depositomina=9999990)
