import django
from django.contrib.auth import hashers
from django.http import HttpResponse
from django.template import Template, Context
from django.template.loader import get_template
from django.shortcuts import redirect, render
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import login_required
from io import StringIO
import json
import datetime
from bdChuntels.forms import RegisterForm, LoginForm , EditForm
from django.contrib.auth.hashers import make_password, check_password
from django.views import View
from django.http import JsonResponse
from bdChuntels.models import User , Friend 

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
                photo = registroUsuario['fotoPerfilUsuario'],
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
        formEdit = EditForm(request.POST , request.FILES)
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
            """
            usuario.age = editData['age']
            if(editData['newCarrear'] != ''):
                usuario.typeCarrear = editData['newCarrear']
            """
            if(editData['newfotoPerfilUsuario'] != ''):
                usuario.photo = editData['newfotoPerfilUsuario']
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

class UserView(View):
    def get(self, request):
        userlist = User.objects.all()
        return JsonResponse(list(userlist.values()), safe=False)
    
class UserViewId(View):
    def get(self, request, iduser):
        user = User.objects.get(iduser=iduser)
        jsonUser = json.dumps(model_to_dict(user), sort_keys=True , default= str)
        return JsonResponse(json.loads(jsonUser), safe=False)


class beFriends(View):
    def post(self, request, iduser1, iduser2):
        user1 = User.objects.get(iduser=iduser1)
        user2 = User.objects.get(iduser=iduser2)
        relation= Friend(user=user1, friend=user2)
        while relation.state <= 4:
            if relation.state == 0:
                print('No se conocen')
            elif relation.state == 1:
                print('Amigos')
            elif relation.state == 2:
                print('Solicitud enviada')
            elif relation.state == 3:
                print('Solicitud recibida')
            elif relation.state == 4:
                print('Solicitud rechazada')
        relation.save()
