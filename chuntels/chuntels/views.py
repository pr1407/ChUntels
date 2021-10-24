from django.http import HttpResponse
from django.template import Template, Context
from django.template.loader import get_template
from django.shortcuts import render


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
        'Components/feed.html',
        {
            "tittle": "Pagina Principal",
        }
    )
    
def publication(request):

    return render(
        request,
        'Components/publication.html',
        {
            "tittle": "Pagina Principal",
        }
    )