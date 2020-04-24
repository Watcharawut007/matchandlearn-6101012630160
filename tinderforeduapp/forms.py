from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *


class SignUpForm(UserCreationForm): #form sign up
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    college = forms.CharField(max_length=100)
    gender = forms.CharField(max_length=20)
    email = forms.EmailField(max_length=150)
    birthday = forms.DateTimeField(label='birthday')
    class Meta:
        model = User #link data in field to keep in user model
        fields = ('username', 'password1', 'password2', 'first_name', 'last_name',
'email', 'college', 'gender','birthday')



class CommentForm(forms.ModelForm): #comment form
    star_score= [
            ('1', '1'),
            ('2', '2'),
            ('3', '3'),
            ('4', '4'),
            ('5', '5'),
        ]
    star = forms.CharField(label="Choose your score", widget=forms.Select(choices=star_score)) #star

    class Meta:
        model = Comment #link data that get from star to comment model
        fields = ('comment','star',)

class AdditionalForm(forms.ModelForm):
    Gender = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
    #age = forms.CharField(max_length=10)
    school = forms.CharField(max_length=100)
    #gender = forms.CharField(label="Choose your gender", widget=forms.Select(choices=Gender))
    class Meta:
        model = UserInfo
        fields = ('school',)
class Editprofileform(forms.ModelForm):#edit profile form


    class Meta:
        model = UserInfo #link data in form to userintfo model
        fields = ['firstname', 'lastname', 'age', 'school', 'gender','birthday' ]

class profilepicture(forms.ModelForm): #change profile picture form
    class Meta:
        model = Profilepicture #link data in form to Profilepicture
        fields = ['images']