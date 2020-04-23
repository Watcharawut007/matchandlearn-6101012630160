from datetime import date

from django.urls import resolve, reverse
from django.test import TestCase
from django.http import HttpRequest
from django.contrib.auth.models import User
from tinderforeduapp.models import *
from django.conf import settings
from tinderforeduapp.views import home_page, personal_profile
from tinderforeduapp import views
class birthday_function_Test(TestCase):
    def test_URL_mapping_to_homepage(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)
    def user_look_at_his_age_and_another_user(self):
        user1 = User.objects.create_user('watcharawut009','hiruma157@hotmail.com','tongu20068')
        user2 = User.objects.create_user('watcharawut007','hiruma158@hotmail.com','tongu4590')
        birthday1 = date(2000,4,24)
        birthday2 = date(1989,4,25)
        user_object1=UserInfo.objects.create(name='watcharawut009', firstname='Watcharawut', lastname='Pornsawat', age='19', school='kmutnb',birthday=birthday1)
        subject_object1 = Subject.objects.create(subject_name='english',keyword_subject='english')
        user_object1.expertise.add(subject_object1)
        picture1 = Profilepicture.objects.create(user=user_object1)

        user_object2 = UserInfo.objects.create(name='watcharawut007', firstname='Kitsanapong', lastname='rodjing',
                                              age='30', school='kmutnb', birthday=birthday2)
        subject_object2 = Subject.objects.create(subject_name='Math2',keyword_subject='math2')
        user_object2.expertise.add(subject_object2)
        picture2 = Profilepicture.objects.create(user=user_object2)
        self.client.force_login(User.objects.get_or_create(username='watcharawut009')[0])
        watch_user_profile = self.client.post('/'+str(user_object1.id)+'/personal_profile/')
        self.assertContains(watch_user_profile, 'age: 19')

        response = self.client.post(reverse('tinder:home'), data={'tutor_find':'Math2','gender': '','school':''})
        self.assertContains(response,"Kitsanapong")
        watch_another_profile = self.client.post('/'+str(user_object2.id)+'/profile/')
        self.assertContains(watch_another_profile,'age: 30')
    def test_user_look_at_his_age_and_another_user_when_1_year_pass(self):
        views.datetime_now=date(2021,4,1)
        user1 = User.objects.create_user('watcharawut009', 'hiruma157@hotmail.com', 'tongu20068')
        user2 = User.objects.create_user('watcharawut007', 'hiruma158@hotmail.com', 'tongu4590')
        birthday1 = date(2000, 4, 24)
        birthday2 = date(1989, 4, 25)
        user_object1 = UserInfo.objects.create(name='watcharawut009', firstname='Watcharawut', lastname='Pornsawat',
                                               age='19', school='kmutnb', birthday=birthday1)
        subject_object1 = Subject.objects.create(subject_name='english', keyword_subject='english')
        user_object1.expertise.add(subject_object1)
        picture1 = Profilepicture.objects.create(user=user_object1)

        user_object2 = UserInfo.objects.create(name='watcharawut007', firstname='Kitsanapong', lastname='rodjing',
                                               age='30', school='kmutnb', birthday=birthday2)
        subject_object2 = Subject.objects.create(subject_name='Math2', keyword_subject='math2')
        user_object2.expertise.add(subject_object2)
        picture2 = Profilepicture.objects.create(user=user_object2)
        self.client.force_login(User.objects.get_or_create(username='watcharawut009')[0])
        self.client.post('/')
        watch_user_profile = self.client.post(reverse('tinder:personal_profile',args=[user_object1.id]))
        print(watch_user_profile.content)
        self.assertContains(watch_user_profile, 'age: 20')
        response = self.client.post(reverse('tinder:home'), data={'tutor_find': 'Math2', 'gender': '', 'school': ''})
        self.assertContains(response, "Kitsanapong")
        watch_another_profile = self.client.post(reverse('tinder:another_profile',args=[user_object2.id]))
        print(watch_another_profile.content)
        self.assertContains(watch_another_profile, 'age: 31')
