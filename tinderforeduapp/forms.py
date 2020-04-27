from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *


class SignUpForm(UserCreationForm): #form sign up
    genderdata = [
        ('male', 'male'),
        ('female', 'female'),
        ('orther', 'orther'),
    ]
    username= forms.CharField(max_length=100,label='Username',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'enter your username','id':'username_id'}))
    password1 = forms.CharField(max_length=100,label='Password',widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'enter your password','id':'password_id','type':'password'}))
    password2 = forms.CharField(max_length=100,label='Password Confirm',widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'enter your password again','id':'password_confirm_id','type':'password'}))
    first_name = forms.CharField(max_length=100,label='First name',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'enter your firstname','id':'firstname_id'}))
    last_name = forms.CharField(max_length=100,label='Last name',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'enter your lastname','id':'lastname_id'}))
    college = forms.CharField(max_length=100,label='College',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'enter the college name','id':'college_id'}))
    gender = forms.CharField(label='gender',widget=forms.Select(attrs={'class':'custom-select','placeholder':'select your gender','id':'id_gender'}))
    email = forms.EmailField(max_length=150,label='Email',widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'example@gmail.com','id':'email_id','type':'Email'}))
    birthday = forms.DateTimeField(label='birthday',widget=forms.DateTimeInput(attrs={'class':'form-control','placeholder':'mm/dd/year','id':'birthday_id'}))
    class Meta:
        model = User #link data in field to keep in user model
        fields=['username','password1','password2','first_name','last_name','college','gender','email','birthday']



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