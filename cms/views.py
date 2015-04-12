from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from models import Pages
from django.views.decorators.csrf import csrf_exempt
from parser_barrapunto import getBarrapunto
import codecs

# Create your views here.

barrapunto = ""

def actualizate(request):
    global barrapunto
    barrapunto = getBarrapunto()
    return HttpResponse("Updating BarraPunto..." + barrapunto)


@csrf_exempt
def handler(request, recurso):
    if request.method == "GET":
        try:
            fila = Pages.objects.get(name=recurso)
            out = fila.name + ": " + fila.page + "<br><hr>" + barrapunto
            return HttpResponse(out)
        except Pages.DoesNotExist:
            return HttpResponseNotFound("Page not found: " + recurso)
    if request.method == "PUT":
            nuevo = Pages(name=recurso, page=request.body)
            nuevo.save()
            return HttpResponse("Saved Page, check it with GET")
    else:
        return HttpResponseNotFound("Method not found: " + request.method)
