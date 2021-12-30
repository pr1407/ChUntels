from django.db import models
from django.db.models.fields.related import ManyToManyField

# Create your models here.
class carrear(models.Model):
    idcarrera = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    def __str__(self):
        return self.nombre
    
class User(models.Model):
    iduser = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50 , unique=True)
    password = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    nickname = models.CharField(max_length=50 , unique=True)
    is_active = models.BooleanField(default=True)
    photo = models.ImageField(upload_to='fotosPerfil/', null=True, blank=True)
    age = models.DateTimeField(auto_now=False)
    typeCarrear = models.ForeignKey(carrear, on_delete=models.CASCADE)
    def __str__(self):
        return self.name

class typePost(models.Model):
    idtypePost = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

class TypeNotification(models.Model):
    idtypenotification = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Notification(models.Model):
    idnotification = models.AutoField(primary_key=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiverNotification')
    typeNotification = models.ForeignKey(TypeNotification, on_delete=models.CASCADE)
    def __str__(self):
        return self.content


class Post(models.Model):
    idpost = models.AutoField(primary_key=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    coments = models.ManyToManyField(User, related_name='comentsPost')
    likes = models.ManyToManyField(User, related_name='likesPost' , blank=True)
    photo = models.ImageField(upload_to='photos/', null=True, blank=True)
    files = models.FileField(upload_to='files/', null=True, blank=True)
    typePost = models.ForeignKey(typePost, on_delete=models.CASCADE)
    
    def num_likes(self):
        return self.likes.count()

class Work(models.Model):
    idwork = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='photos/', null=True, blank=True)
    files = models.FileField(upload_to='files/', null=True, blank=True)
    cocreators = models.ManyToManyField(User, related_name='cocreatorsWork')
    typePost = models.ForeignKey(typePost, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='likesWork' , blank=True)
    coments = models.ManyToManyField(User, related_name='comentsWork')
    def num_likes(self):
        return self.likes.count()

class Coments(models.Model):
    idcoment = models.AutoField(primary_key=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comentsPost')
    likes = models.ManyToManyField(User, related_name='likesComents', blank=True)
    photo = models.ImageField(upload_to='photos/', null=True, blank=True)
    files = models.FileField(upload_to='files/', null=True, blank=True)
    def num_likes(self):
        return self.likes.count()

class ComentsWorks(models.Model):
    idcoment = models.AutoField(primary_key=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    work = models.ForeignKey(Work, on_delete=models.CASCADE, related_name='comentsWorks')
    likes = models.ManyToManyField(User, related_name='likesComentsWorks', blank=True)
    photo = models.ImageField(upload_to='photos/', null=True, blank=True)
    files = models.FileField(upload_to='files/', null=True, blank=True)
    def num_likes(self):
        return self.likes.count()

class Friend(models.Model):
    idfriend = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE , related_name='personUser')
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend')
    state = models.CharField(max_length=1 , default='0')


class Chat(models.Model):
    idchat = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiverChat')

class Message(models.Model):
    idmessage = models.AutoField(primary_key=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver', null=True)
    photo = models.ImageField(upload_to='photos/', null=True, blank=True)
    files = models.FileField(upload_to='files/', null=True, blank=True)
    state = models.CharField(max_length=1, default='1', null=True, blank=True)

class Files(models.Model):
    idfile = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='photos/', null=True, blank=True)
    files = models.FileField(upload_to='files/', null=True, blank=True)