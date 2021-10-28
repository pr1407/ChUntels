from django import forms

from bdChuntels.models import carrear
import datetime 

class DateInput(forms.DateInput):
    input_type = 'date'


class RegisterForm(forms.Form):
    
    username = forms.CharField(label='Username', max_length=100)
    email = forms.EmailField(label='Email')
    password = forms.CharField(label='Password', widget=forms.PasswordInput())
    nickname = forms.CharField(label='Nickname', max_length=100)
    fotoPerfilUsuario = forms.ImageField(label='Foto de perfil', widget=forms.FileInput() , required=False)
    nacimiento = forms.DateField(label='Fecha Nacimiento' , widget=DateInput())
    carrear = forms.ModelChoiceField(label='Carrera', queryset=carrear.objects.all())


class LoginForm(forms.Form):
    email = forms.EmailField(label='Email')
    password = forms.CharField(label='Password', widget=forms.PasswordInput())


class EditForm(forms.Form):
    newUsername = forms.CharField(label='Username', max_length=100 , required=False)
    newEmail = forms.EmailField(label='Email' , required=False)
    newNickname = forms.CharField(label='Nickname', max_length=100 , required=False)
    newPassword = forms.CharField(label='Password', widget=forms.PasswordInput() , required=False)
    newfotoPerfilUsuario = forms.ImageField(label='Foto de perfil', widget=forms.FileInput() , required=False)
    newCarrear = forms.ModelChoiceField(label='Carrera', queryset=carrear.objects.all() , required=False)