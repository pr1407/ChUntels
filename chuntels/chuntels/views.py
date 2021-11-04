import django
from django import forms
from django.contrib.auth import hashers
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
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

today = datetime.date.today()

def register(request):


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
    
    
    else:
        formRegistro = RegisterForm()
    
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


def home(request):

    if 'user' in request.session:

        user = User.objects.get(iduser = request.session['user'])
        resta = today.year - user.age.year
        return render(
            request,
            'Home/home.html',
            {
                "user" : user,  
                "resta" : resta,
                "tittle": "Pagina Principal",
            }
        )
    return redirect('/login')


def logout(request):
    if 'user' in request.session:
        del request.session['user']
    return redirect('/login')



def changeData(request):
    user = User.objects.get(iduser=request.session['user'])
    formEdit = EditForm()
    
    if request.method == 'POST':
        formEdit = EditForm(request.POST , request.FILES)
        if formEdit.is_valid():
            editData = formEdit.cleaned_data
            
            if(editData['newUsername'] != ''):
                user.name = editData['newUsername']
            if(editData['newEmail'] != ''):
                user.email = editData['newEmail']
            if(editData['newNickname'] != ''):
                user.nickname = editData['newNickname']
            if(editData['newPassword'] != ''):
                user.password = make_password(editData['newPassword'], salt=None, hasher='default')
            """
            usuario.age = editData['age']
            if(editData['newCarrear'] != ''):
                usuario.typeCarrear = editData['newCarrear']
            """
            if(editData['newfotoPerfilUsuario'] is not None):
                user.photo = editData['newfotoPerfilUsuario']
            user.save()
            return redirect('/home')

    return render(
            request,
            'Home/cambiarDatos.html',
            {
                "tittle": "Cambiar Datos", 
                "form": formEdit,
                "user" : user
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

def perfilUser(request,nickname):
    userSesion = User.objects.get(iduser=request.session['user'])
    userProfile = User.objects.get(nickname=nickname)
    resta = today.year - userProfile.age.year
    return render(
        request,
        'PerfilFriend/PerfilFriend.html',
        {
            "user": userSesion,
            "userProfile" : userProfile,
            "edad": resta,
            "tittle": userProfile.nickname,
        }
    )

class UserView(View):
    def get(self, request):
        userlist = User.objects.all()
        return JsonResponse(list(userlist.values()), safe=False)
    
# Busqueda Usuario    
class UserViewId(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)   

    def get(self, request, iduser):
        user = User.objects.get(iduser=iduser)
        
        jsonUser = json.dumps(model_to_dict(user), sort_keys=True , default= str)
        return JsonResponse(json.loads(jsonUser), safe=False)

    def post(self, request, iduser):
        print (request.POST)
        user = User.objects.get(iduser=iduser)
        jsonUser = json.dumps(model_to_dict(user), sort_keys=True , default= str)
        datos = {"mensaje": "envio" , "datos" : json.loads(jsonUser)}
        print(datos)
        return JsonResponse(datos, safe=False)

class UserViewName(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)   

    def get(self, request, name):
        user = User.objects.get(name=name)
        
        jsonUser = json.dumps(model_to_dict(user), sort_keys=True , default= str)
        return JsonResponse(json.loads(jsonUser), safe=False)
        
    def post(self, request):
        print(request.POST)

        if request.POST.get('nombre') == '':
            datos = {"valor":False,"mensaje": "No se encontró resultados" , "data" : {}}
            return JsonResponse(datos, safe=False)
        
        try:
            user = User.objects.filter(name__contains=request.POST.get('nombre'))
            
            jsonUser = json.dumps(list(user.values()), sort_keys=True , default= str)
            datos = {"valor":True,"mensaje": "Lista de personas" , "data" : json.loads(jsonUser)}
        except:
            datos = {"valor":False,"mensaje": "No se encontró resultados" , "data" : {}}
        #print(datos)
        ###datos = {"valor":True,"mensaje": "envio" , "datos" : request.POST.get('nombre')}
        return JsonResponse(datos, safe=False)

class UserViewNickName(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)   

    def get(self, request, nickname):
        user = User.objects.get(nickname=nickname)
        
        jsonUser = json.dumps(model_to_dict(user), sort_keys=True , default= str)
        return JsonResponse(json.loads(jsonUser), safe=False)

    def post(self, request, nickname):
        print (request.POST)
        user = User.objects.get(nickname=nickname)
        jsonUser = json.dumps(model_to_dict(user), sort_keys=True , default= str)
        datos = {"mensaje": "envio" , "datos" : json.loads(jsonUser)}
        print(datos)
        return JsonResponse(datos, safe=False)

class beFriends(View):
    def post(self, request, iduser1, iduser2):
        if iduser1 != iduser2:
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
