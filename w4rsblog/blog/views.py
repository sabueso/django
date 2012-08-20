from django.template import Context, loader
from django.shortcuts import render_to_response
from w4rsblog.blog.models import Articulos
from django.http import HttpResponse

#def index(request):
#    recuentodeobjetos = Articulos.objects.all().order_by('fecha')[:10]
#    output = '\n,'.join([p.cuerpo for p in recuentodeobjetos])
#    return HttpResponse(output)

#def index(request):
#    	recuentodeobjetos = Articulos.objects.all().order_by('-fecha')[:20]
#    	t = loader.get_template('blog/index.html')
#	c = Context({
#        'recuentodeobjetos': recuentodeobjetos,
#   })
#	return HttpResponse(t.render(c))


def index(request):
	recuentodeobjetos = Articulos.objects.all().order_by('-fecha')[:20]
	return render_to_response('blog/index.html', {'recuentodeobjetos': recuentodeobjetos})

def detalle(request,articulos_id):
	try:
		p=Articulos.objects.get(pk=articulos_id)
	except Articulos.DoesNotExist:
		raise Http404
	return render_to_response('blog/detalle.html',{'articulo':p})
