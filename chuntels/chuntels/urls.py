"""chuntels URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from chuntels.views import login,home,feed,publication,service, register, changeData , logout , \
UserView ,UserViewName, UserViewNickName , perfilUser, chat,beFriends
urlpatterns = [

    path('admin/', admin.site.urls),
    path('login/', login),
    path('register/', register),
    path('home/', home),
    path('feed/', feed),
    path('chat/', chat),
    path('publication/<int:id>/', publication),
    path('api/saludo/', service),
    path('editdata/',changeData),
    path('logout/', logout),
    path('user/', UserView.as_view() , name= 'userList'),
    path('user/<str:nickname>/', perfilUser, name= 'userDetail'),
    path('api/search-person/', UserViewName.as_view() , name= 'userDetail'),
    path('api/send-friend-request/', beFriends.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


