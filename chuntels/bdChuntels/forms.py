from django import forms
from django.forms.fields import ChoiceField
from django.forms.widgets import ChoiceWidget, SelectMultiple
from bdChuntels.models import User
from bdChuntels.models import carrear
import datetime 

class DateInput(forms.DateInput):
    input_type = 'date'


class RegisterForm(forms.Form):
    
    username = forms.CharField(label='Username',widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Username'}), max_length=100)
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control','placeholder': 'Email'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': 'Password'}))
    nickname = forms.CharField(label='Nickname',widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Nickname'}), max_length=100)
    fotoPerfilUsuario = forms.ImageField(label='Foto de perfil', widget=forms.FileInput() , required=False)
    nacimiento = forms.DateField(label='Fecha Nacimiento' , widget=DateInput(attrs={'class': 'form-control','placeholder': 'Fecha Nacimiento'}))
    carrear = forms.ModelChoiceField(label='Carrera', widget=forms.Select(attrs={'class': 'form-control','placeholder': 'Carrera'}), queryset=carrear.objects.all())


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Username'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': 'Password'}))


class EditForm(forms.Form):
    newUsername = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=100 , required=False)
    newEmail = forms.EmailField(label='Email' , widget=forms.EmailInput(attrs={'class': 'form-control'}), required=False)
    newNickname = forms.CharField(label='Nickname', widget=forms.TextInput(attrs={'class': 'form-control'}),max_length=100 , required=False)
    newPassword = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}) , required=False)
    newfotoPerfilUsuario = forms.ImageField(label='Foto de perfil', widget=forms.FileInput(attrs={'class': 'form-control'}) , required=False)
    #newCarrear = forms.ModelChoiceField(label='Carrera', queryset=carrear.objects.all() , required=False)newfotoPerfilUsuario