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
from bdChuntels.models import User , Friend , Post , typePost

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

def chat(request):

    if 'user' in request.session:

        user = User.objects.get(iduser = request.session['user'])
        resta = today.year - user.age.year
        return render(
            request,
            'Chat/chat.html',
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

    if 'user' in request.session:

        user = User.objects.get(iduser = request.session['user'])
        resta = today.year - user.age.year
        return render(
            request,
            'Feed/feed.html',
            {
                "user" : user,  
                "resta" : resta,
                "tittle": "Pagina Principal",
            }
        )
    return redirect('/login')
    
def publication(request,id):

    if 'user' in request.session:

        user = User.objects.get(iduser = request.session['user'])
        resta = today.year - user.age.year
        return render(
            request,
            'Publication/publication.html',
            {
                "user" : user,  
                "resta" : resta,
                "tittle": "Pagina Principal",
            }
        )
    return redirect('/login')

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
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)   
    

    def post(self, request):
        user = request.POST.get('user')
        friend = request.POST.get('friend')
        state = request.POST.get('state')
        
        try:
            relacionInversa = Friend.objects.get(user=friend, friend=user)
            datos = {"valor":False,"mensaje": "Ya esta amigos" , "data" : {}}
            relacionInversa.state = state
            if relacionInversa.state == '1':
                datos = {"valor":True,"mensaje": "Recibiste una solicitud" , "data" : {}}
            if relacionInversa.state == '2':
                datos = {"valor":True,"mensaje": "Aceptaste la solicitud" , "data" : {}}
            if relacionInversa.state == '3':
                datos = {"valor":True,"mensaje": "Negaste la solicitud" , "data" : {}}
            relacionInversa.save()
            return JsonResponse(datos, safe=False)
        except:
            relacionInversa = None
            datos = {"valor":False,"mensaje": "No existe una relacion" , "data" : {}}
        
        try:
            relacion = Friend.objects.get(user=user,friend=friend)
            jsonrelation = json.dumps(model_to_dict(relacion), sort_keys=True , default= str)
            datos = {"valor":False,"mensaje": "Ya se envio la solicitud" , "data" : json.loads(jsonrelation)}
        except:
            relacion = None
            datos = {"valor":False,"mensaje": "No existe una relacion" , "data" : {}}
        
        if relacion == None:
            if user != friend:
                relation = Friend(user=User.objects.get(iduser = user) , friend=User.objects.get(iduser = friend))
                relation.state = "1" 
                if relation.state == '1':
                    datos = {"valor":True,"mensaje": "Se ha enviado la solicitud" , "data" : {}}
                    relation.save()
            else:
                datos = {"valor":False,"mensaje": "No se puede enviar la solicitud" , "data" : {}}
        else:
            relacion.state = state
            if relacion.state == '1':
                datos = {"valor":True,"mensaje": "Se ha enviado la solicitud" , "data" : {}}
            if relacion.state == '2':
                datos = {"valor":True,"mensaje": "Se ha aceptado la solicitud" , "data" : {}}
            if relacion.state == '3':
                datos = {"valor":True,"mensaje": "Se ha negado la solicitud" , "data" : {}}           
            
            relacion.save()

        return JsonResponse(datos, safe=False)

class sendPublication(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)   

    def post(self, request):

        user = request.POST.get('user')
        publication = request.POST.get('publication')
        photo = request.POST.get('photo')
        files = request.POST.get('files')
        _typePost = request.POST.get('typePost')

        if user == None or user == '':
            datos = {"valor":False,"mensaje": "No se encontró usuario" , "data" : {}}
            return JsonResponse(datos, safe=False)

        if publication == None or publication == '':
            datos = {"valor":False,"mensaje": "Debes ingresar al menos 1 caracter o archivo" , "data" : {}}
            return JsonResponse(datos, safe=False)
        
        if _typePost == None or _typePost == '':
            _typePost = typePost.objects.get(idtypePost=1)
        else:
            _typePost = typePost.objects.get(idtypePost=_typePost)

        try :
            user = User.objects.get(iduser=user)
            send_post = Post(
                content = publication,
                created_at = today,
                user = user,
                typePost = _typePost
            )

            if photo != None or photo != '':
                send_post.photo = photo

            if photo != None or photo != '':
                send_post.files = files
            
            response = send_post.save()

            datos = {"valor":True,"mensaje": "Publicacion realizada" , "data" : {}}

        except ValueError:
            datos = {"valor":False,"mensaje": "No se pudo enviar la publicacion" , "data" : {}}

        return JsonResponse(datos, safe=False)

class getPublication(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        try:
            nickname = request.GET.get('nickname',1)
            if nickname==1 or nickname=='1':
                nickname = User.objects.get(iduser=request.session['user']).nickname
                print("USUARIO: "+str(nickname))
            user = User.objects.get(nickname=nickname)

            post = Post.objects.filter(user=user)

            jsonPost = json.dumps(list(post.values()), sort_keys=True , default= str)

            datos = {"valor":True,"mensaje": "Lista de publicaciones" , "data" : json.loads(jsonPost)}
        except:
            datos = {"valor":False,"mensaje": "No se encontró resultados" , "data" : {}}

        return JsonResponse(datos, safe=False)

