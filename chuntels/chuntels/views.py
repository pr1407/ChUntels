from django.contrib.auth import hashers
from django.http import HttpResponse
from django.template import Template, Context
from django.template.loader import get_template
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from io import StringIO
import json
import datetime
from bdChuntels.forms import RegisterForm, LoginForm , EditForm
from django.contrib.auth.hashers import make_password, check_password
from bdChuntels.models import User

def register(request):

    formRegistro = RegisterForm()

    today = datetime.date.today()


    if request.method == 'POST':

        formRegistro = RegisterForm(request.POST)

        if formRegistro.is_valid():
            registroUsuario = formRegistro.cleaned_data
            usuario = User.objects.create(
                name = registroUsuario['username'],
                email = registroUsuario['email'],
                password = make_password(registroUsuario['password'], salt=None, hasher='default'), 
                created_at = today,
                nickname = registroUsuario['nickname'],
                #photo = registroUsuario['fotoPerfilUsuario'],
                age = registroUsuario['nacimiento'],
                typeCarrear = registroUsuario['carrear']
            )

            usuario.save()

            return redirect('/login')
    
    return render(
            request,
                'Login/register.html',
                {
                    "tittle": "Pagina Registro", 
                    "form": formRegistro
                }
            ) 

   
def login(request):

    formLogin = LoginForm() 

    if request.method == 'POST':

        formLogin = LoginForm(request.POST)

        if formLogin.is_valid():
            loginUsuario = formLogin.cleaned_data
            usuario = User.objects.get(email = loginUsuario['email'])
            if check_password(loginUsuario['password'], usuario.password):
                request.session['user'] = usuario.iduser
                return redirect('/home')
            else:
                return redirect('/login')   

    return render(  
        request,
        'Login/login.html',
        {
            "tittle": "Pagina login", 
            "form": formLogin
        }
    )

@login_required(login_url='/login')
def home(request):
    if 'user' in request.session:
        return render(
            request,
            'Home/home.html',
            {
                "tittle": "Pagina Principal",
            }
        )
    else: 
        return redirect('/login')



@login_required(login_url='/login')
def logout(request):
    if 'user' in request.session:
        del request.session['user']
    return redirect('/login')



@login_required(login_url='/login')
def changeData(request):
    
    formEdit = EditForm()
    
    if request.method == 'POST':
        formEdit = EditForm(request.POST)
        if formEdit.is_valid():
            editData = formEdit.cleaned_data
            usuario = User.objects.get(iduser=request.session['user'])
            if(editData['newUsername'] != ''):
                usuario.name = editData['newUsername']
            if(editData['newEmail'] != ''):
                usuario.email = editData['newEmail']
            if(editData['newNickname'] != ''):
                usuario.nickname = editData['newNickname']
            if(editData['newPassword'] != ''):
                usuario.password = make_password(editData['newPassword'], salt=None, hasher='default')
            #usuario.age = editData['age']
            if(editData['newCarrear'] != ''):
                usuario.typeCarrear = editData['newCarrear']
            
            usuario.save()
            return redirect('/home')

    return render(
            request,
            'Home/cambiarDatos.html',
            {
                "tittle": "Cambiar Datos", 
                "form": formEdit
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