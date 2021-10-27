from django import forms

from bdChuntels.models import carrear

class RegisterForm(forms.Form):
    
    username = forms.CharField(label='Username', max_length=100)
    email = forms.EmailField(label='Email')
    password = forms.CharField(label='Password', widget=forms.PasswordInput())
    nickname = forms.CharField(label='Nickname', max_length=100)
    #fotoPerfilUsuario = forms.ImageField(label='Foto de perfil')
    edad = forms.IntegerField(label='Edad')
    carrear = forms.ModelChoiceField(label='Carrera', queryset=carrear.objects.all())