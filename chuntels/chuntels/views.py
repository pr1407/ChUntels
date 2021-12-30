import django
from django import forms
from django.contrib.auth import hashers
from django.conf import settings
from django.http import HttpResponse, Http404
import os
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
from bdChuntels.models import *
import timeago

today = datetime.date.today()


def redirectLogin(request):
    return redirect('/login')

def register(request):

    if 'user' in request.session:
        return redirect('/home')
        
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

    if 'user' in request.session:
        return redirect('/home')

    formLogin = LoginForm() 

    if request.method == 'POST':

        formLogin = LoginForm(request.POST)

        if formLogin.is_valid():
            loginUsuario = formLogin.cleaned_data
            try:
                usuario = User.objects.get(name = loginUsuario['username'])
                if check_password(loginUsuario['password'], usuario.password):
                    usuario.is_active = True
                    usuario.save(update_fields=['is_active'])
                    request.session['user'] = usuario.iduser
                    return redirect('/home')
                else:
                    return redirect('/login')
            except User.DoesNotExist:
                #return redirect('/login')
                print("error")
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
        posts = Post.objects.filter(user = user)
        friends = Friend.objects.filter(user = user) | Friend.objects.filter(friend = user)
        resta = today.year - user.age.year
        return render(
            request,
            'Home/home.html',
            {
                "user" : user,  
                "posts" : posts,  
                "friends" : friends,  
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
        print(request.session['user'])
        user = User.objects.get(iduser = request.session['user'])
        user.is_active = False
        user.save(update_fields=['is_active'])

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
        post = Post.objects.get(idpost = id)

        now = datetime.datetime.now()

        fecha = timeago.format(datetime.datetime.date(post.created_at),now)

        post.created_at = fecha

        resta = today.year - user.age.year
        return render(
            request,
            'Publication/publication.html',
            {
                "user" : user,  
                "resta" : resta,
                "data" : post,
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

    relationstate = '0'
    reseiver = userProfile

    try:
        relation = Friend.objects.get(user=userSesion, friend=userProfile)
        relationstate = relation.state
        reseiver = userProfile
    except Friend.DoesNotExist:
        relation = None
        
    if relationstate == '0':
        try:
            relation = Friend.objects.get(user=userProfile, friend=userSesion)
            relationstate = relation.state
            reseiver = userSesion
        except Friend.DoesNotExist:
            relation = None

    return render(
        request,
        'PerfilFriend/PerfilFriend.html',
        {
            "user": userSesion,
            "userProfile" : userProfile,
            "edad": resta,
            "tittle": userProfile.nickname,
            "relation": relationstate,
            "reseiver": reseiver
        }
    )

# Servicios 

class UserView(View):
    def get(self, request):
        userlist = User.objects.all()
        return JsonResponse(list(userlist.values()), safe=False)
 
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
        except Exception as e:
            datos = {"valor":False,"mensaje": "No se encontró resultados" , "data" : str(e)}
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
        user =request.session['user']
        friend = request.POST.get('friend')
        state = request.POST.get('state')
        
        try:
            relacionInversa = Friend.objects.get(user=friend, friend=user)
            datos = {"valor":False,"mensaje": "Ya son amigos" , "data" : {}}
            relacionInversa.state = state
            if relacionInversa.state == '1':
                datos = {"valor":True,"mensaje": "Recibiste una solicitud" , "data" : {}}
                noti = Notification.objects.create(
                    content="Te han enviado una solicitud de amistad",
                    created_at = today,
                    user=User.objects.get(iduser = user) , 
                    receiver=User.objects.get(iduser = friend) , 
                    typeNotification = TypeNotification.objects.get(idtypenotification = 1)
                )
                noti.save()
            if relacionInversa.state == '2':
                datos = {"valor":True,"mensaje": "Aceptaste la solicitud" , "data" : {}}
                existeChat = Chat.objects.filter(user=User.objects.get(iduser = user) , receiver=User.objects.get(iduser = friend)) | Chat.objects.filter(user=User.objects.get(iduser = friend) , receiver=User.objects.get(iduser = user)) 
                print(existeChat)
                listavacia= list(existeChat)
                if listavacia:                
                    datos = {"valor":False,"mensaje": "El chat ya existe" , "data" : {}}
                else:
                    chat = chat = Chat.objects.create(user=User.objects.get(iduser = user) , receiver=User.objects.get(iduser = friend))
                    chat.save()
                    datos = {"valor":True,"mensaje": "Creando Chat" , "data" : {}}
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
                
                noti = Notification.objects.create(
                    content="Te han enviado una solicitud de amistad",
                    created_at = today,
                    user= User.objects.get(iduser = user) , 
                    receiver= User.objects.get(iduser = friend) , 
                    typeNotification = TypeNotification.objects.get(idtypenotification = 1)
                )
                noti.save()
            if relacion.state == '2':
                datos = {"valor":True,"mensaje": "Se ha aceptado la solicitud" , "data" : {}}
                existeChat = Chat.objects.filter(user=User.objects.get(iduser = user) , receiver=User.objects.get(iduser = friend)) | Chat.objects.filter(user=User.objects.get(iduser = friend) , receiver=User.objects.get(iduser = user)) 
                listavacia= list(existeChat)
                if listavacia:                
                    datos = {"valor":False,"mensaje": "El chat ya existe" , "data" : {}}
                else:
                    chat = chat = Chat.objects.create(user=User.objects.get(iduser = user) , receiver=User.objects.get(iduser = friend))
                    chat.save()
                    datos = {"valor":False,"mensaje": "Creando Chat" , "data" : {}}
            if relacion.state == '3':
                datos = {"valor":True,"mensaje": "Se ha negado la solicitud" , "data" : {}}           
            
            relacion.save()

        return JsonResponse(datos, safe=False)

class deletePublication(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)   

    def post(self, request):
        user =request.session['user']
        idPublication = request.POST.get('idPublication')
        try:
            publication = Post.objects.get(idpost = idPublication)
            publication.delete()
            datos = {"valor":True,"mensaje": "Se ha eliminado la publicacion" , "data" : {}}
        except Exception as e:
            datos = {"valor":False,"mensaje": "No se pudo eliminar la publicacion" , "data" : str(e)}
        return JsonResponse(datos, safe=False)

class sendPublication(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)   

    def post(self, request):

        user =request.session['user']
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
            _typePost = typePost.objects.get(idtypePost=2)
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
            
            send_post.save()

            datos = {"valor":True,"mensaje": "Publicacion realizada" , "data" : {}}

        except Exception as e:
            datos = {"valor":False,"mensaje": "No se pudo enviar la publicacion" , "data" : str(e)}

        return JsonResponse(datos, safe=False)

class sendWork(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)   

    def post(self, request):

        user =request.session['user']
        nameWork = request.POST.get('name')
        workcontent = request.POST.get('contenido')
        photo = request.POST.get('photo')
        files = request.POST.get('files')
        _typePost = request.POST.get('typePost')

        if user == None or user == '':
            datos = {"valor":False,"mensaje": "No se encontró usuario" , "data" : {}}
            return JsonResponse(datos, safe=False)

        if workcontent == None or workcontent == '':
            datos = {"valor":False,"mensaje": "Debes ingresar al menos 1 caracter o archivo" , "data" : {}}
            return JsonResponse(datos, safe=False)
        
        if _typePost == None or _typePost == '':
            _typePost = typePost.objects.get(idtypePost=1)
        else:
            _typePost = typePost.objects.get(idtypePost=_typePost)

        try :
            user = User.objects.get(iduser=user)
            send_work = Work(
                name = nameWork,
                description = workcontent,
                created_at = today,
                user = user,
                typePost = _typePost
            )

            if photo != None or photo != '':
                send_work.photo = photo

            if photo != None or photo != '':
                send_work.files = files
            
            send_work.save()

            datos = {"valor":True,"mensaje": "Trabajo creado" , "data" : {}}

        except Exception as e:
            datos = {"valor":False,"mensaje": "No se pudo crear el trabajo" , "data" : str(e)}

        return JsonResponse(datos, safe=False)

class sendCocreators(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    def post(self, request):
        cocreator = User.objects.get(iduser=request.POST.get('cocreator'))
        work = Work.objects.get(idwork=request.POST.get('work'))
        listCocreators = work.cocreators.filter(iduser=cocreator.iduser)
        creatorWork = User.objects.get(iduser=work.user.iduser)
        try:
            listavacia= list(listCocreators)
            if cocreator != creatorWork:
                print(listavacia)
                if listavacia:                
                    work.cocreators.remove(cocreator)
                    work.save()
                    datos = {"valor":False,"mensaje": "Quitando colaborador" , "data" : {}}
                else:
                    work.cocreators.add(cocreator)
                    work.save()
                    datos = {"valor":False,"mensaje": "Agregando colaborador" , "data" : {}}
            else:
                datos = {"valor":False,"mensaje": "No puedes agregarte a ti mismo" , "data" : {}}
        except Exception as e:
            datos = {"valor":False,"mensaje": "No se pudo agregar al colaborador" , "data" : str(e)}
        return JsonResponse(datos, safe=False)

class getWorks(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    def post(self, request):
        user = User.objects.get(iduser=request.session['user'])
        works = Work.objects.filter(user=user)
        try:      
            jsonWorksUser = json.dumps(list(works.values()), sort_keys=True , default= str)
            datos = {"valor":True,"mensaje": "Lista de trabajos" , "data" :{ "Trabajos" : json.loads(jsonWorksUser)} }
        except Exception as e:
            datos = {"valor":False,"mensaje": "No se encontraron likes" , "data" : str(e) }
        return JsonResponse(datos, safe=False)

class getColaboratorsWorks(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    def post(self, request):
        work = Work.objects.get(idwork=request.POST.get('idwork'))
        userLikes = work.cocreators.all()
        values = userLikes.values()
        try:      
            for value in values:
                del value['iduser']
                del value['password']
                del value['created_at']
            jsonListCoworks = json.dumps(list(values), sort_keys=True , default= str)
            datos = {"valor":True,"mensaje": "Lista de trabajos" , "data" :{"colaboladores":json.loads(jsonListCoworks) , "cantidad" : work.cocreators.count()} }
        except Exception as e:
            datos = {"valor":False,"mensaje": "No se encontraron likes" , "data" : str(e)}
        return JsonResponse(datos, safe=False)  

class doLikeWork(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    def post(self, request):
        user = User.objects.get(iduser=request.session['user'])
        work = Work.objects.get(idpost=request.POST.get('idpublication'))
        userDoLike = work.likes.filter(iduser=user.iduser)
        try:
            listavacia= list(userDoLike)
            print(listavacia)
            if listavacia:                
                work.likes.remove(user)
                work.save()
                datos = {"valor":False,"mensaje": "Quitando like a esta publicacion" , "data" : {}}
            else:
                work.likes.add(user)
                work.save()
                datos = {"valor":False,"mensaje": "Dando like a esta publicacion" , "data" : {}}
        except Exception as e:
            datos = {"valor":False,"mensaje": "No se pudo realizar el like" , "data" : str(e)}
        return JsonResponse(datos, safe=False)
    
class getPublication(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        try:
            nickname = User.objects.get(iduser=request.session['user']).nickname
            
            user = User.objects.get(nickname=nickname)
            post = Post.objects.filter(user=user)


            jsonPost = json.dumps(list(post.values()), sort_keys=True , default= str)

            datos = {"valor":True,"mensaje": "Lista de publicaciones" , "data" : json.loads(jsonPost)}
        except:
            datos = {"valor":False,"mensaje": "No se encontró resultados" , "data" : {}}

        return JsonResponse(datos, safe=False)
    def post(self, request):
        try:
            user = User.objects.get(nickname=request.POST.get('user'))
            post = Post.objects.filter(user=user)
            jsonPost = json.dumps(list(post.values()), sort_keys=True , default= str)

            datos = {"valor":True,"mensaje": "Lista de publicaciones" , "data" : json.loads(jsonPost)}
        except Exception as e:
            datos = {"valor":False,"mensaje": "No se encontró resultados" , "data" : str(e)}
        return JsonResponse(datos, safe=False)

class getNotification(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        try:
            user = User.objects.get(iduser=request.session['user'])
            notification = Notification.objects.filter(user=user)
            values=notification.values()
            for value in values:
                receiver = value['receiver_id']
                friend = User.objects.filter(iduser=receiver)
                receiver = friend.values()
                del value['receiver_id']
                for rec in receiver:
                    del rec['password']
                    del rec['created_at']
                    carrera = carrear.objects.filter(idcarrera=rec['typeCarrear_id'])
                    rec['carrera'] = carrera.values()[0]['nombre']
                    del rec['typeCarrear_id']
                
                value['receiver'] = receiver[0]

            jsonNotification = json.dumps(list(values), sort_keys=True , default= str)

            datos = {"valor":True,"mensaje": "Lista de notificaciones" , "data" : json.loads(jsonNotification)}
        except Exception as e:
            datos = {"valor":False,"mensaje": "No se encontró resultados" , "data" : str(e)}

        return JsonResponse(datos, safe=False)
    def post(self, request):
        try:
            user = User.objects.get(iduser=request.POST.get('user'))
            notification = Notification.objects.filter(user=user)
            values= notification.values()
            for value in values:
                receiver = value['receiver_id']
                friend = User.objects.filter(iduser=receiver)
                receiver = friend.values()
                del value['receiver_id']
                for rec in receiver:
                    del rec['password']
                    del rec['created_at']
                    carrera = carrear.objects.filter(idcarrera=rec['typeCarrear_id'])
                    rec['carrera'] = carrera.values()[0]['nombre']
                    del rec['typeCarrear_id']
                
                value['receiver'] = receiver[0]
            
            """listReceiver = values['receiver_id']
            friend = User.objects.filter(iduser=listReceiver)
            print(friend)"""
            jsonNotification = json.dumps(list(values), sort_keys=True , default= str)

            datos = {"valor":True,"mensaje": "Lista de notificaciones" , "data" : json.loads(jsonNotification)}
        except Exception as e:
            datos = {"valor":False,"mensaje": "No se encontró resultados" , "data" : str(e)}

        return JsonResponse(datos, safe=False)

class getFriends(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    def get(self, request):
        try:
            user = User.objects.get(iduser=request.session['user'])
            friends = Friend.objects.filter(user = user , state='2') | Friend.objects.filter(friend = user , state='2')
            values = friends.values()
            for value in values:
                useR = value['user_id']
                frienD = value['friend_id']
                if useR == user.iduser:
                    friend = User.objects.filter(iduser=frienD)
                    frienD = friend.values()
                    for fri in frienD:
                        del fri['password']
                        del fri['created_at']
                        carrera = carrear.objects.filter(idcarrera=fri['typeCarrear_id'])
                        fri['carrera'] = carrera.values()[0]['nombre']
                        del fri['typeCarrear_id']

                    value['friend'] = frienD[0]
                else:
                    friend = User.objects.filter(iduser=useR)
                    useR = friend.values()
                    for fri in useR:
                        del fri['password']
                        del fri['created_at']
                        carrera = carrear.objects.filter(idcarrera=fri['typeCarrear_id'])
                        fri['carrera'] = carrera.values()[0]['nombre']
                        del fri['typeCarrear_id']
                    value['friend'] = useR[0]
                del value['user_id']
                del value['friend_id']
                del value['idfriend']  
            jsonFriends = json.dumps(list(values), sort_keys=True , default= str)

            datos = {"valor":True,"mensaje": "Lista de amigos" , "data" : json.loads(jsonFriends)}
        except:
            datos = {"valor":False,"mensaje": "No se encontró resultados" , "data" : {}}
        return JsonResponse(datos, safe=False)
    
    def post(self, request):
        try:
            user = User.objects.get(iduser=request.POST.get('user'))
            friends = Friend.objects.filter(user = user , state='2') | Friend.objects.filter(friend = user , state='2')
            values = friends.values()
            for value in values:
                useR = value['user_id']
                frienD = value['friend_id']
                if useR == user.iduser:
                    friend = User.objects.filter(iduser=frienD)
                    frienD = friend.values()
                    for fri in frienD:
                        del fri['password']
                        del fri['created_at']
                        carrera = carrear.objects.filter(idcarrera=fri['typeCarrear_id'])
                        fri['carrera'] = carrera.values()[0]['nombre']
                        del fri['typeCarrear_id']

                    value['friend'] = frienD[0]
                else:
                    friend = User.objects.filter(iduser=useR)
                    useR = friend.values()
                    for fri in useR:
                        del fri['password']
                        del fri['created_at']
                        carrera = carrear.objects.filter(idcarrera=fri['typeCarrear_id'])
                        fri['carrera'] = carrera.values()[0]['nombre']
                        del fri['typeCarrear_id']
                    value['friend'] = useR[0]
                del value['user_id']
                del value['friend_id']
                del value['idfriend']  
            jsonFriends = json.dumps(list(values), sort_keys=True , default= str)

            datos = {"valor":True,"mensaje": "Lista de amigos" , "data" : json.loads(jsonFriends)}
        except Exception as e:
            datos = {"valor":False,"mensaje": "No se encontró resultados" , "data" : str(e)}
        return JsonResponse(datos, safe=False)

class getFriendPublications(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    def get(self, request):
        try:
            user = User.objects.get(iduser=request.session['user'])
            friends = Friend.objects.filter(user = user , state='2') | Friend.objects.filter(friend = user , state='2')
            listPublicFriends = []
            for friend in friends:
                if friend.friend.iduser == user.iduser:
                    PostFriends = Post.objects.filter(user = friend.user)
                else:
                    PostFriends = Post.objects.filter(user = friend.friend)
                values = PostFriends.values()
                for value in values:
                    publiuser = User.objects.filter(iduser=value['user_id'])
                    publiuser = publiuser.values()[0]
                    del publiuser['password']
                    del publiuser['iduser']
                    value['user'] = publiuser
                    del value['user_id']
                listPublicFriends += list(values)
            jsonFriendPublications = json.dumps(listPublicFriends, sort_keys=True , default= str)
            datos = {"valor":True,"mensaje": "Lista de publicaciones de amigos" , "data" : json.loads(jsonFriendPublications)}
        except:
            datos = {"valor":False,"mensaje": "No se encontraron publicaciones de amigos" , "data" : {}}
        return JsonResponse(datos, safe=False)
    def post(self, request):
        try:
            user = User.objects.get(iduser=request.POST.get('user'))
            friends = Friend.objects.filter(user = user , state='2') | Friend.objects.filter(friend = user , state='2')
            for friend in friends:
                if friend.friend.iduser == user.iduser:
                    PostFriends = Post.objects.filter(user = friend.user)
                else:
                    PostFriends = Post.objects.filter(user = friend.friend)
                values = PostFriends.values()
            jsonFriendPublications = json.dumps(list(values), sort_keys=True , default= str)
            datos = {"valor":True,"mensaje": "Lista de publicaciones de amigos" , "data" : json.loads(jsonFriendPublications)}
        except Exception as e:
            datos = {"valor":False,"mensaje": "No se encontraron publicaciones de amigos" , "data" : str(e)}
        return JsonResponse(datos, safe=False)

class comentPublication(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    def post(self, request):
        user = User.objects.get(iduser=request.session['user'])
        post = request.POST.get('idpublication')
        comentcontent = request.POST.get('coment')
        photo = request.POST.get('photo')
        files = request.POST.get('files')
        try:
            post = Post.objects.get(idpost=post)
            coment = Coments(
                content = comentcontent,
                created_at = today,
                user = user,
                post = post
            )
            if photo != None or photo != '':
                coment.photo = photo
            
            if files != None or files != '':
                coment.files = files

            coment.save()
            datos = {"valor":True,"mensaje": "Comentario realizado" , "data" : {}}
        except Exception as e:
            datos = {"valor":False,"mensaje": "No se pudo realizar el comentario" , "data" : str(e)}
        return JsonResponse(datos, safe=False)

class getPublicationComents(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    def get(self, request):
        try:
            post = request.GET.get('idpublication')
            post = Post.objects.get(idpost=post)
            coments = Coments.objects.filter(post=post)
            values = coments.values()
            for value in values:
                receiver = value['user_id']
                user = User.objects.filter(iduser=receiver)
                receiver = user.values()
                del value['user_id']
                for rec in receiver:
                    del rec['password']
                    del rec['created_at']
                    carrera = carrear.objects.filter(idcarrera=rec['typeCarrear_id'])
                    rec['carrera'] = carrera.values()[0]['nombre']
                    del rec['typeCarrear_id']
                value['usuario creador'] = receiver[0]
            jsonComents = json.dumps(list(values), sort_keys=True , default= str)
            datos = {"valor":True,"mensaje": "Lista de comentarios" , "data" : json.loads(jsonComents)}
        except:
            datos = {"valor":False,"mensaje": "No se encontraron comentarios" , "data" : {}}
        return JsonResponse(datos, safe=False)
    def post(self, request):
        try: 
            post = request.POST.get('idpost')
            post = Post.objects.get(idpost=post)
            coments = Coments.objects.filter(post=post)
            values = coments.values()
            for value in values:
                receiver = value['user_id']
                user = User.objects.filter(iduser=receiver)
                receiver = user.values()
                del value['user_id']
                for rec in receiver:
                    del rec['password']
                    del rec['created_at']
                    carrera = carrear.objects.filter(idcarrera=rec['typeCarrear_id'])
                    rec['carrera'] = carrera.values()[0]['nombre']
                    del rec['typeCarrear_id']
                value['usuario_creador'] = receiver[0]
            jsonComents = json.dumps(list(values), sort_keys=True , default= str)
            datos = {"valor":True,"mensaje": "Lista de comentarios" , "data" : json.loads(jsonComents)}
        except Exception as e:
            datos = {"valor":False,"mensaje": "No se encontraron comentarios" , "data" : str(e)}
        return JsonResponse(datos, safe=False)

class doLikePost(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    def post(self, request):
        user = User.objects.get(iduser=request.session['user'])
        post = Post.objects.get(idpost=request.POST.get('idpublication'))
        userDoLike = post.likes.filter(iduser=user.iduser)
        try:
            listavacia= list(userDoLike)
            print(listavacia)
            if listavacia:                
                post.likes.remove(user)
                post.save()
                datos = {"valor":True,"mensaje": "Quitando like a esta publicacion" , "data" : {}}
            else:
                post.likes.add(user)
                post.save()
                datos = {"valor":True,"mensaje": "Dando like a esta publicacion" , "data" : {}}
        except Exception as e:
            datos = {"valor":False,"mensaje": "No se pudo realizar el like" , "data" : str(e)}
        return JsonResponse(datos, safe=False)

class getLikesPost(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    def get(self, request):
        post = Post.objects.get(idpost = request.GET.get('idpublication'))
        userLikes = post.likes.all()
        values = userLikes.values()
        try:      
            for value in values:
                del value['iduser']
                del value['password']
                del value['created_at']
            jsonLikesPost = json.dumps(list(values), sort_keys=True , default= str)
            
            datos = {"valor":True,"mensaje": "Lista de likes" , "data" :{ "usuarios":json.loads(jsonLikesPost) , "cantidad" : post.likes.count()} }
        except:
            datos = {"valor":False,"mensaje": "No se encontraron likes" , "data" : {}}
        return JsonResponse(datos, safe=False)
    def post(self, request):
        post = Post.objects.get(idpost=request.POST.get('idpublication'))
        userLikes = post.likes.all()
        values = userLikes.values()
        try:      
            for value in values:
                del value['iduser']
                del value['password']
                del value['created_at']
            jsonLikesPost = json.dumps(list(values), sort_keys=True , default= str)
            
            datos = {"valor":True,"mensaje": "Lista de likes" , "data" :{ "usuarios":json.loads(jsonLikesPost) , "cantidad" : post.likes.count()} }
        except Exception as e:
            datos = {"valor":False,"mensaje": "No se encontraron likes" , "data" : str(e)}
        return JsonResponse(datos, safe=False)
        
class getLikesWorks(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        work = Work.objects.get(idwork = request.GET.get('idwork'))
        userLikes = work.likes.all()
        values = userLikes.values()
        try:      
            for value in values:
                del value['iduser']
                del value['password']
                del value['created_at']
            jsonLikesWorks = json.dumps(list(values), sort_keys=True , default= str)
            
            datos = {"valor":True,"mensaje": "Lista de likes" , "data" :{ "usuarios":json.loads(jsonLikesWorks) , "cantidad" : work.likes.count()} }
        except:
            datos = {"valor":False,"mensaje": "No se encontraron likes" , "data" : {}}
        return JsonResponse(datos, safe=False)
    def post(self, request):
        work = Work.objects.get(idwork=request.POST.get('idwork'))
        userLikes = work.likes.all()
        values = userLikes.values()
        try:      
            for value in values:
                del value['iduser']
                del value['password']
                del value['created_at']
            jsonLikesWorks = json.dumps(list(values), sort_keys=True , default= str)
            
            datos = {"valor":True,"mensaje": "Lista de likes" , "data" :{ "usuarios":json.loads(jsonLikesWorks) , "cantidad" : work.likes.count()} }
        except Exception as e:
            datos = {"valor":False,"mensaje": "No se encontraron likes" , "data" : str(e)}
        return JsonResponse(datos, safe=False)

#Funciona
class doLikeComents(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    def post(self, request):
        user = User.objects.get(iduser=request.session['user'])
        coment = Coments.objects.get(idcoment=request.POST.get('coment'))
        userDoLike = coment.likes.filter(iduser=user.iduser)
        try:
            listavacia= list(userDoLike)
            print(listavacia)
            if listavacia:                
                coment.likes.remove(user)
                coment.save()
                datos = {"valor":False,"mensaje": "Quitando like a este comentario" , "data" : {}}
            else:
                coment.likes.add(user)
                coment.save()
                datos = {"valor":False,"mensaje": "Dando like a este comentario" , "data" : {}}
        except Exception as e:
            datos = {"valor":False,"mensaje": "No se pudo realizar el like" , "data" : str(e)}
        return JsonResponse(datos, safe=False)

#Funciona
class getLikeComents(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    def post(self, request):
        coment = Coments.objects.get(idcoment=request.POST.get('coment'))
        userLikes = coment.likes.all()
        values = userLikes.values()
        try:      
            for value in values:
                del value['iduser']
                del value['password']
                del value['created_at']
            jsonLikesComents = json.dumps(list(values), sort_keys=True , default= str)
            
            datos = {"valor":True,"mensaje": "Lista de likes" , "data" :{ "usuarios":json.loads(jsonLikesComents) , "cantidad" : coment.likes.count()} }
        except Exception as e:
            datos = {"valor":False,"mensaje": "No se encontraron likes" , "data" : str(e)}
        return JsonResponse(datos, safe=False)
#Funciona
class comentWorks(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    def post(self, request):
        user = User.objects.get(iduser=request.session['user'])
        work = request.POST.get('work')
        coment = request.POST.get('coment')
        photo = request.POST.get('photo')
        files = request.POST.get('files')
        try:
            work = Work.objects.get(idwork=work)
            coment = ComentsWorks(
                content = coment,
                created_at = today,
                user = user,
                work = work
            )
            
            if photo != None or photo != '':
                coment.photo = photo
            
            if files != None or files != '':
                coment.files = files

            coment.save()
            datos = {"valor":True,"mensaje": "Comentario al trabajo realizado" , "data" : {}}
        except Exception as e:
            datos = {"valor":False,"mensaje": "No se pudo realizar el comentario al trabajo" , "data" : str(e)}
        return JsonResponse(datos, safe=False)

#Funciona
class getWorksComents(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    def get(self, request):
        try:
            work = Work.objects.get(idpost=request.GET.get('work'))
            coments = ComentsWorks.objects.filter(work=work)
            values = coments.values()
            for value in values:
                receiver = value['user_id']
                user = User.objects.filter(iduser=receiver)
                receiver = user.values()
                del value['user_id']
                for rec in receiver:
                    del rec['password']
                    del rec['created_at']
                    carrera = carrear.objects.filter(idcarrera=rec['typeCarrear_id'])
                    rec['carrera'] = carrera.values()[0]['nombre']
                    del rec['typeCarrear_id']
                value['usuario creador'] = receiver[0]
            jsonComents = json.dumps(list(values), sort_keys=True , default= str)
            datos = {"valor":True,"mensaje": "Lista de comentarios" , "data" : json.loads(jsonComents)}
        except:
            datos = {"valor":False,"mensaje": "No se encontraron comentarios" , "data" : {}}
        return JsonResponse(datos, safe=False)
    def post(self, request):
        try: 
            work = Work.objects.get(idwork=request.POST.get('work'))
            coments = ComentsWorks.objects.filter(work=work)
            values = coments.values()
            for value in values:
                receiver = value['user_id']
                user = User.objects.filter(iduser=receiver)
                receiver = user.values()
                del value['user_id']
                for rec in receiver:
                    del rec['password']
                    del rec['created_at']
                    carrera = carrear.objects.filter(idcarrera=rec['typeCarrear_id'])
                    rec['carrera'] = carrera.values()[0]['nombre']
                    del rec['typeCarrear_id']
                value['usuario creador'] = receiver[0]
            jsonComents = json.dumps(list(values), sort_keys=True , default= str)
            datos = {"valor":True,"mensaje": "Lista de comentarios" , "data" : json.loads(jsonComents)}
        except Exception as e:
            datos = {"valor":False,"mensaje": "No se encontraron comentarios" , "data" : str(e)}
        return JsonResponse(datos, safe=False)

#Funciona
class doLikeComentsWorks(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    def post(self, request):
        user = User.objects.get(iduser=request.session['user'])
        coment = ComentsWorks.objects.get(idcoment=request.POST.get('coment'))
        print(coment)
        userDoLike = coment.likes.filter(iduser=user.iduser)
        try:
            listavacia= list(userDoLike)
            if listavacia:                
                coment.likes.remove(user)
                coment.save()
                datos = {"valor":False,"mensaje": "Quitando like a este comentario de trabajo" , "data" : {}}
            else:
                coment.likes.add(user)
                coment.save()
                datos = {"valor":False,"mensaje": "Dando like a este comentario de trabajo" , "data" : {}}
        except Exception as e:
            datos = {"valor":False,"mensaje": "No se pudo realizar el like" , "data" : str(e)}
        return JsonResponse(datos, safe=False)

#Funciona
class getLikeComentsWorks(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    def post(self, request):
        coment = ComentsWorks.objects.get(idcoment=request.POST.get('coment'))
        userLikes = coment.likes.all()
        values = userLikes.values()
        
        try:      
            for value in values:
                del value['iduser']
                del value['password']
                del value['created_at']
            jsonLikesComents = json.dumps(list(values), sort_keys=True , default= str)
            
            datos = {"valor":True,"mensaje": "Lista de likes" , "data" :{ "usuarios":json.loads(jsonLikesComents) , "cantidad" : coment.likes.count()} }
        except:
            datos = {"valor":False,"mensaje": "No se encontraron likes" , "data" : {}}
        return JsonResponse(datos, safe=False)

class sendMessages(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    def post(self, request):
        try:
            user = User.objects.get(iduser=request.session['user'])
            receiver = User.objects.get(iduser=request.POST.get('friend'))
            message = request.POST.get('message')
            today = datetime.datetime.now()
            message = Message(
                content = message,
                created_at = today,
                user = user,
                receiver = receiver,
                state = '1'
            )
            message.save()
            datos = {"valor":True,"mensaje": "Mensaje enviado" , "data" : {}}
        except Exception as e:
            datos = {"valor":False,"mensaje": "No se pudo enviar el mensaje" , "data" : {}}
            return HttpResponse(e)
        return JsonResponse(datos, safe=False)


class getMessages(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    def post(self, request):
        try:
            now = datetime.datetime.now()

            user = User.objects.get(iduser=request.session['user'])
            friend = User.objects.get(iduser=request.POST.get('friend'))
            messages = Message.objects.filter(receiver=user,user=friend,state='1').order_by('created_at') | Message.objects.filter(user=user,receiver=friend,state='1').order_by('created_at')
            values = messages.values()
            for value in values:
                value['created_at'] = timeago.format(datetime.datetime.date(value['created_at']),now)

                if value['user_id'] == request.session['user']:
                    value['user_id'] = user.nickname
                else:
                    value['user_id'] = friend.nickname
                
                del value['idmessage']
                del value['receiver_id']

            jsonMessages = json.dumps(list(values), sort_keys=True , default= str)
            datos = {"valor":True,"mensaje": "Lista de mensajes" , "data" : json.loads(jsonMessages)}
        except Exception as e:
            datos = {"valor":False,"mensaje": "No se encontraron mensajes" , "data" : {}}
            return HttpResponse(e)
        return JsonResponse(datos, safe=False)

class uploadFiles(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    def post(self, request):
        try:
            user = User.objects.get(iduser=request.session['user'])
            requestfile = request.FILES['file']
            today = datetime.datetime.now()
            file = Files(
                name = requestfile.name,
                created_at = today,
                user = user
            )
            url = ""

            if "PNG" in requestfile.name or "JPG" in requestfile.name or "JPEG" in requestfile.name or "GIF" in requestfile.name or "png" in requestfile.name or "jpg" in requestfile.name or "jpeg" in requestfile.name or "gif" in requestfile.name:
                url = "/photos/" + requestfile.name
                tipofile = "photo"
                file.photo = requestfile
            else:
                url = "/files/" + requestfile.name
                tipofile = "file"
                file.files = requestfile

            file.save()
            #return HttpResponse(file.name)
            datos = {"valor":True,"mensaje": "Archivo subido" , "data" : {"url":url,"type":tipofile}}
        except Exception as e:
            datos = {"valor":False,"mensaje": "No se pudo subir el archivo" , "data" : {}}
            return HttpResponse(e)
        return JsonResponse(datos, safe=False)

def download(request, path):
    file_path = os.path.join(settings.MEDIA_ROOT,'files/'+ path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-Excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404