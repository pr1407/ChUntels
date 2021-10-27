from django.http import HttpResponse
from django.template import Template, Context
from django.template.loader import get_template
from django.shortcuts import redirect, render
from io import StringIO
import json
import datetime
from bdChuntels.forms import RegisterForm

from bdChuntels.models import User

def register(request):

    formRegistro= RegisterForm()

    if request.method == 'POST':

        formRegistro = RegisterForm(request.POST)

        if formRegistro.is_valid():
            registroUsuario = formRegistro.cleaned_data
            usuario = User.objects.create(
                name = registroUsuario['username'],
                email = registroUsuario['email'],
                password = registroUsuario['password'],
                created_at = datetime.date.today(),
                nickname = registroUsuario['nickname'],
                #photo = registroUsuario['fotoPerfilUsuario'],
                age = registroUsuario['edad'],
                typeCarrear = registroUsuario['carrear']
            )

            usuario.save()

            return redirect('/login')
    
    return render(
            request,
                'Login/register.html',
                {
                    "tittle": "Pagina Registro", "form": formRegistro
                }
            ) 
    
def login(request):

    return render(
        request,
        'Login/login.html',
        {
            "tittle": "Pagina login",
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