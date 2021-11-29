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
from chuntels.views import *
urlpatterns = [
    path('', redirectLogin),

    #WEB PHAT'S
    path('admin/', admin.site.urls),
    path('login/', login),
    path('register/', register),
    path('home/', home),
    path('feed/', feed),
    path('publication/<int:id>/', publication),
    path('api/saludo/', service),
    path('editdata/',changeData),
    path('logout/', logout),
    path('user/', UserView.as_view() , name= 'userList'),
    path('user/<str:nickname>/', perfilUser, name= 'userDetail'),

    #API REST PHAT'S
    path('api/search-person/', UserViewName.as_view() , name= 'userDetail'),
    path('api/send-friend-request/', beFriends.as_view()),
    path('api/send-publication/', sendPublication.as_view()),
    path('api/get-publication/<str:nickname>/', getPublication.as_view()),
    path('api/get-publication/', getPublication.as_view()),
    path('api/get-notifications/', getNotification.as_view()),
    path('api/get-friends/', getFriends.as_view() , name= 'userDetail'),
    path('api/get-friends/<str:nickname>/', getFriends.as_view() , name= 'userDetail'),
    path('api/get-friends-publications/', getFriendPublications.as_view()),
    path('api/coment-publication/', comentPublication.as_view()),
    path('api/get-publication-coments/', getPublicationComents.as_view()),
    path('api/send-likes-post/', doLikePost.as_view()),
    path('api/get-likes-post/', getLikesPost.as_view()),
    path('api/send-work/', sendWork.as_view()),
    path('api/get-work/', getWorks.as_view()),
    path('api/send-colaborators-work/', sendCocreators.as_view()),
    path('api/get-colaborators-work/', getColaboratorsWorks.as_view()),
    path('api/send-likes-work/', doLikeWork.as_view()),
    path('api/get-likes-work/', getLikesWorks.as_view()),
    path('api/send-likes-coment/', doLikeComents.as_view()),
    path('api/get-likes-coment/', getLikeComents.as_view()),
    path('api/send-coments-work/', comentWorks.as_view()),
    path('api/get-coments-work/', getWorksComents.as_view()),
    path('api/send-likes-comentsworks/', doLikeComentsWorks.as_view()),
    path('api/get-likes-comentsworks/', getLikeComentsWorks.as_view()),
    path('chat/',chat),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
