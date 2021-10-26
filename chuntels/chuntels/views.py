from django.http import HttpResponse
from django.template import Template, Context
from django.template.loader import get_template
from django.shortcuts import render
from io import StringIO
import json

def login(request):

    return render(
        request,
        'Login/login.html',
        {
            "tittle": "Pagina Principal",
        }
    )

def home(request):

    return render(
        request,
        'Home/home.html',
        {
            "tittle": "Pagina Principal",
        }
    )

def feed(request):

    return render(
        request,
        'Feed/feed.html',
        {
            "tittle": "Pagina Principal",
        }
    )
    
def publication(request):

    return render(
        request,
        'Publication/publication.html',
        {
            "tittle": "Pagina Principal",
        }
    )

def service(request):

    responce = {}

    if request.method == 'POST':
        responce = {
            "valor":True,
            "msn":'Hola!',
            "data":{'nombre':'Juan','apellido':'Perez'}
        }
    else:
        responce = {
            "valor":False,
            "msn":'Chau!',
            "data":{}
        }    
    
    jsonResponse = json.dumps(responce, sort_keys=True)

    return HttpResponse(jsonResponse)