from django.db import models

# Create your models here.
class carrear(models.Model):
    idcarrera = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)

class User(models.Model):
    iduser = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    nickname = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    photo = models.ImageField(upload_to='photos/', null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    typeCarrear = models.ForeignKey(carrear, on_delete=models.CASCADE)

class typePost(models.Model):
    idtypePost = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

class TypeNotification(models.Model):
    idtypenotification = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=50)

class Notification(models.Model):
    idnotification = models.AutoField(primary_key=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiverNotification')
    typeNotification = models.ForeignKey(TypeNotification, on_delete=models.CASCADE)

class Post(models.Model):
    idpost = models.AutoField(primary_key=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    coments = models.ManyToManyField(User, related_name='comentsPost')
    likes = models.ManyToManyField(User, related_name='likesPost')
    photo = models.ImageField(upload_to='photos/', null=True, blank=True)
    files = models.FileField(upload_to='files/', null=True, blank=True)
    typePost = models.ForeignKey(typePost, on_delete=models.CASCADE)

class Coments(models.Model):
    idcoment = models.AutoField(primary_key=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comentsPost')
    likes = models.ManyToManyField(User, related_name='likesComents')
    photo = models.ImageField(upload_to='photos/', null=True, blank=True)
    files = models.FileField(upload_to='files/', null=True, blank=True)

class Follow(models.Model):
    idfollow = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')

class Like(models.Model):
    idlike = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    coment = models.ForeignKey(Coments, on_delete=models.CASCADE)

class Friend(models.Model):
    idfriend = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE , related_name='personUser')
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend')

class stateMessage(models.Model):
    idstateMessage = models.AutoField(primary_key=True)
    state =models.CharField(max_length=50)

class Chat(models.Model):
    idchat = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiverChat')

class Message(models.Model):
    idmessage = models.AutoField(primary_key=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiverMessage')
    photo = models.ImageField(upload_to='photos/', null=True, blank=True)
    files = models.FileField(upload_to='files/', null=True, blank=True)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    state = models.ForeignKey(stateMessage, on_delete=models.CASCADE)


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
    likes = models.ManyToManyField(User, related_name='likesWork')
    coments = models.ManyToManyField(User, related_name='comentsWork')