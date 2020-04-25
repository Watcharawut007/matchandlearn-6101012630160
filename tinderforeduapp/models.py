from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime
# Create your models here.


class Subject(models.Model): #create subject model
    subject_name = models.TextField(max_length=200, blank=True) #Collect a subject data when user add it
    keyword_subject = models.TextField(max_length=200, blank=True) #Collect a subject_name value in lower case for easily to search
    def __str__(self):
        return self.subject_name


class Requestmodel(models.Model):#create request model
    who_send = models.TextField(max_length=200, blank=True)#Collect a url_room_name who sent a request
    request_message = models.TextField(max_length=600,blank=True)#Collect about me data
    who_recive = models.TextField(max_length=200, blank=True)#Collect a url_room_name who will recive a request
    def __str__(self):
        return self.who_send
class Matchmodel(models.Model):#creat match model
    myself = models.TextField(max_length=200, blank=True) #Collect a url_room_name user
    another_user = models.TextField(max_length=200, blank=True)#Collect a url_room_name who matched with this user
    def __str__(self):
        return self.myself

class UserInfo(models.Model):#create user information model
    name = models.TextField(max_length=200, blank=True)#Collect a username data
    firstname = models.TextField(max_length=200, blank=True)#Collect a first url_room_name
    lastname = models.TextField(max_length=200, blank=True)#Collect a last url_room_name
    age = models.TextField(max_length=10,blank=True)#Collect a age
    school = models.TextField(max_length=200,blank=True)#Collect a school url_room_name
    school_keyword = models.TextField(max_length=200, blank=True)#get a value from school variable a convert to upper case for easily to search
    gender = models.TextField(blank=True)#Collect a gender
    fb_link = models.TextField(null=True)#Collect a facebook link
    expertise = models.ManyToManyField(Subject, related_name='Userinfos', blank=True)#enable to link this model to subject model
    request = models.ManyToManyField(Requestmodel, blank=True)#enable to link this model to request model
    match = models.ManyToManyField(Matchmodel, blank=True)#enable to link this model to match model
    match_request = models.IntegerField(default=0)#Collect amount of notify when you have a request from someone
    message_list = models.IntegerField(default=0)#Collect amount of notify when you have a message from someone
    birthday = models.DateTimeField(blank=True)#Collect birthday
    def __str__(self):
        return self.name
    def read(self):#its mean when you go to request list then amount of notify will be zero
        self.match_request = 0
        self.save()
    def notify(self):#when you have request amount of notify should be increase
        self.match_request = self.match_request + 1
        self.save()

    def denotify(self):#when someone cancel request amount of notify should be decrease
        self.match_request = self.match_request - 1
        self.save()
    def check_birthday(self, date):#check birthday if today is the user birthday then update age
        if (self.birthday.day <= date.day and self.birthday.month <= date.month) or self.birthday.month < date.month:#when user birthday passed in this year
             self.age = str(date.year - self.birthday.year)
             self.save()
        elif (self.birthday.day > date.day and self.birthday.month >= date.month) or self.birthday.month > date.month:#when user birthday has not passed in this year
             self.age = str(date.year - self.birthday.year-1)
             self.save()


class Comment(models.Model):#create comment model
    post = models.ForeignKey(UserInfo, on_delete=models.CASCADE, related_name='comments', null=True)#link this model to userinfo
    name = models.CharField(max_length=80,null=True)#Collect  who comment you
    comment = models.CharField(max_length=500,null=True)#Collect a comment message
    star = models.CharField(max_length=500,null=True)#Collect a score
    created_on = models.DateTimeField(auto_now_add=True,null=True)
    active = models.BooleanField(default=True,null=True)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment to {} by {}'.format(self.post, self.name)

class Profile(models.Model):#create a profile model,this model is same Userinfo model,this model is create for when user register then this model keep a information
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    college = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=150)
    age = models.TextField(max_length=10, blank=True)
    bio = models.TextField()
    birthday = models.DateTimeField(default=datetime.now,blank=True)
    def __str__(self):
        return self.user.username
class Profilepicture(models.Model):#this model create for Profile picture
    user = models.OneToOneField(UserInfo, on_delete=models.CASCADE)#Collect a first url_room_name
    images = models.ImageField(default='default.png',upload_to='media')#Collect a picture




















@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
