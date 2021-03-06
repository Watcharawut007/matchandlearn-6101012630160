from datetime import date

from django.core.management import call_command
from django.urls import resolve, reverse
from django.test import TestCase

from django.contrib.auth.models import User
from tinderforeduapp.models import *
from django.conf import settings
from tinderforeduapp.views import home_page, personal_profile
from django.contrib.auth.views import LoginView
from tinderforeduapp import views
class birthday_function_Test(TestCase):

    def user_look_at_his_age_and_another_user(self):
        views.datetime_now = date(2020, 4, 1) #today is 1/4/2020
        # 2 users is signin
        watcharawut = User.objects.create_user('watcharawut009','hiruma157@hotmail.com','tongu20068')
        kitsanapong = User.objects.create_user('watcharawut007','hiruma158@hotmail.com','tongu4590')
        birthday1 = date(2000,4,24)#the user1 birthday
        birthday2 = date(1989,4,25)#the user2 birthday

        # his name is watcharawut and his expertise subject is english
        watcharawut_user=UserInfo.objects.create(name='watcharawut009', firstname='Watcharawut', lastname='Pornsawat', age='19', school='kmutnb',birthday=birthday1)
        subject_object1 = Subject.objects.create(subject_name='english',keyword_subject='english')
        watcharawut_user.expertise.add(subject_object1)

        #load profile picture watcharawut(this first time that he use this website profile picture is default.png)
        picture1 = Profilepicture.objects.create(user=watcharawut_user)

        # his name is kitsanapong and his expertise subject is math2
        kitsanapong_user = UserInfo.objects.create(name='watcharawut007', firstname='Kitsanapong', lastname='rodjing',
                                              age='30', school='kmutnb', birthday=birthday2)
        subject_object2 = Subject.objects.create(subject_name='Math2',keyword_subject='math2')
        kitsanapong_user.expertise.add(subject_object2)

        # load profile picture kitsanapong(this first time that he use this website profile picture is default.png)
        picture2 = Profilepicture.objects.create(user=kitsanapong_user)

        #watcharawut logins
        self.client.force_login(User.objects.get_or_create(username='watcharawut009')[0])

        #he watch his profile and see his age is 19
        watch_user_profile = self.client.post('/'+str(watcharawut_user.id)+'/personal_profile/')
        self.assertContains(watch_user_profile, 'age: 19')

        #he want to find a tutor to teach math2 and he found Kitsanapong
        search_result = self.client.post(reverse('tinder:home'), data={'tutor_find':'Math2','gender': '','school':''})
        self.assertContains(search_result,"Kitsanapong")

        #he watch kitsanapong profile and see his age is 30
        watch_another_profile = self.client.post('/'+str(kitsanapong_user.id)+'/profile/')
        self.assertContains(watch_another_profile,'age: 30')

    def user_look_at_his_age_and_another_user_when_1_year_pass(self):
        views.datetime_now = date(2021, 4, 1)  # today is 1/4/2020
        # 2 users is signin
        watcharawut = User.objects.create_user('watcharawut009', 'hiruma157@hotmail.com', 'tongu20068')
        kitsanapong = User.objects.create_user('watcharawut007', 'hiruma158@hotmail.com', 'tongu4590')
        birthday1 = date(2000, 4, 24)  # the watcharawut birthday
        birthday2 = date(1989, 4, 25)  # the kitsanapong birthday

        # his name is watcharawut his age is 19 and expertise subject is english
        watcharawut_user = UserInfo.objects.create(name='watcharawut009', firstname='Watcharawut', lastname='Pornsawat',
                                                   age='19', school='kmutnb', birthday=birthday1)
        subject_object1 = Subject.objects.create(subject_name='english', keyword_subject='english')
        watcharawut_user.expertise.add(subject_object1)

        # load profile picture watcharawut(this first time that he use this website profile picture is default.png)
        picture1 = Profilepicture.objects.create(user=watcharawut_user)

        # his name is kitsanapong his age is 30 and expertise subject is math2
        kitsanapong_user = UserInfo.objects.create(name='watcharawut007', firstname='Kitsanapong', lastname='rodjing',
                                                   age='30', school='kmutnb', birthday=birthday2)
        subject_object2 = Subject.objects.create(subject_name='Math2', keyword_subject='math2')
        kitsanapong_user.expertise.add(subject_object2)

        # load profile picture kitsanapong(this first time that he use this website profile picture is default.png)
        picture2 = Profilepicture.objects.create(user=kitsanapong_user)

        # watcharawut logins
        self.client.force_login(User.objects.get_or_create(username='watcharawut009')[0])

        # he watch his profile and see his age is 20
        watch_user_profile = self.client.post('/' + str(watcharawut_user.id) + '/personal_profile/')
        self.assertContains(watch_user_profile, 'age: 20')

        # he want to find a tutor to teach math2 and he found Kitsanapong
        search_result = self.client.post(reverse('tinder:home'), data={'tutor_find': 'Math2', 'gender': '', 'school': ''})
        self.assertContains(search_result, "Kitsanapong")

        # he watch kitsanapong profile and see his age is 31
        watch_another_profile = self.client.post('/' + str(kitsanapong_user.id) + '/profile/')
        self.assertContains(watch_another_profile, 'age: 31')

    def test_user_can_comment_to_another_user_who_matched_with_him_and_can_delete_it(self):
        # 2 users is signin
        watcharawut = User.objects.create_user('watcharawut009', 'hiruma157@hotmail.com', 'tongu20068')
        kitsanapong = User.objects.create_user('watcharawut007', 'hiruma158@hotmail.com', 'tongu4590')
        birthday1 = date(2000, 4, 24)  # the watcharawut birthday
        birthday2 = date(1989, 4, 25)  # the kitsanapong birthday

        # his name is watcharawut his age is 19 and expertise subject is english
        watcharawut_user = UserInfo.objects.create(name='watcharawut009', firstname='Watcharawut', lastname='Pornsawat',
                                                   age='19', school='kmutnb', birthday=birthday1)
        subject_object1 = Subject.objects.create(subject_name='english', keyword_subject='english')
        watcharawut_user.expertise.add(subject_object1)

        # load profile picture watcharawut(this first time that he use this website profile picture is default.png)
        picture1 = Profilepicture.objects.create(user=watcharawut_user)

        # his name is kitsanapong his age is 30 and expertise subject is math2
        kitsanapong_user = UserInfo.objects.create(name='watcharawut007', firstname='Kitsanapong', lastname='rodjing',
                                                   age='30', school='kmutnb', birthday=birthday2)
        subject_object2 = Subject.objects.create(subject_name='Math2', keyword_subject='math2')
        kitsanapong_user.expertise.add(subject_object2)

        #2 user match each orther
        match_list_watcharawut = Matchmodel.objects.create(myself=watcharawut_user.name,
                                                           another_user=kitsanapong_user.name)
        watcharawut_user.match.add(match_list_watcharawut)

        match_list_kitsanapong = Matchmodel.objects.create(myself=kitsanapong_user.name,
                                                           another_user=watcharawut_user.name)
        kitsanapong_user.match.add(match_list_kitsanapong)
        # load profile picture kitsanapong(this first time that he use this website profile picture is default.png)
        picture2 = Profilepicture.objects.create(user=kitsanapong_user)

        # watcharawut logins
        self.client.force_login(User.objects.get_or_create(username='watcharawut009')[0])

        # he watch his profile and see his age is 20
        watch_tutor_student_profile = self.client.post('/'+'tutor_student_list/')
        self.assertContains(watch_tutor_student_profile,'Kitsanapong rodjing')

        watch_kitsanpong_profile = self.client.post('/' + str(kitsanapong_user.id) + '/watch_profile/')
        self.assertContains(watch_kitsanpong_profile,kitsanapong_user.firstname)
        add_comment_kitsanpong_profile = self.client.post(reverse('tinder:create_comment',args=[kitsanapong_user.id]),data={'comment': 'he is a good teacher', 'star': '5'},follow=True)
        self.assertContains(add_comment_kitsanpong_profile,'he is a good teacher')
        comment_obj = Comment.objects.get(post=kitsanapong_user,name=watcharawut_user.name,comment='he is a good teacher',)
        remove_comment_kitsanapong_profile = self.client.post(reverse('tinder:delete_comment',args=[kitsanapong_user.id]),{watcharawut_user.firstname+'_delete_comment':str(comment_obj.id)},follow=True)
        self.assertNotContains(remove_comment_kitsanapong_profile,'he is a good teacher')





class user_is_authenticated(TestCase):

    def test_when_user_do_not_login(self):
        watcharawut = User.objects.create_user('watcharawut009', 'hiruma157@hotmail.com', 'tongu20068')
        kitsanapong = User.objects.create_user('watcharawut007', 'hiruma158@hotmail.com', 'tongu4590')
        birthday1 = date(2000, 4, 24)  # the watcharawut birthday
        birthday2 = date(1989, 4, 25)  # the kitsanapong birthday

        # his name is watcharawut his age is 19 and expertise subject is english
        watcharawut_user = UserInfo.objects.create(name='watcharawut009', firstname='Watcharawut', lastname='Pornsawat',
                                                   age='19', school='kmutnb', birthday=birthday1)
        subject_object1 = Subject.objects.create(subject_name='english', keyword_subject='english')
        watcharawut_user.expertise.add(subject_object1)

        # load profile picture watcharawut(this first time that he use this website profile picture is default.png)
        picture1 = Profilepicture.objects.create(user=watcharawut_user)

        # his name is kitsanapong his age is 30 and expertise subject is math2
        kitsanapong_user = UserInfo.objects.create(name='watcharawut007', firstname='Kitsanapong', lastname='rodjing',
                                                   age='30', school='kmutnb', birthday=birthday2)
        subject_object2 = Subject.objects.create(subject_name='Math2', keyword_subject='math2')
        kitsanapong_user.expertise.add(subject_object2)

        #load profile picture kitsanapong(this first time that he use this website profile picture is default.png)
        picture2 = Profilepicture.objects.create(user=kitsanapong_user)


        # anonymous people who does not login try to connect in to this website with enter url

        # anonymous people enter personal profile url for watch kitsanapong profile
        respone_personal_profile=self.client.post(reverse('tinder:personal_profile'),follow=True)

        # if he can not go in,templates will show a login template that have a link to sign up
        self.assertContains(respone_personal_profile,'New to Match and Learn? Sign up now!')
        self.assertTemplateUsed(respone_personal_profile,'registration/login.html')

        # anonymous people enter watch profile url for watch to kitsanapong profile
        respone_watch_profile = self.client.post(reverse('tinder:watch_profile', args=[kitsanapong_user.id]),
                                                    follow=True)

        # if he can not go in,templates will show a login template that have a link to sign up
        self.assertContains(respone_personal_profile, 'New to Match and Learn? Sign up now!')
        self.assertTemplateUsed(respone_personal_profile, 'registration/login.html')

        # anonymous people enter tutor student list url for see people that kitsanapong matched
        respone_tutor_student_lists = self.client.post(reverse('tinder:tutor_student_list'),
                                                    follow=True)

        # if he can not go in,templates will show a login template that have a link to sign up
        self.assertContains(respone_tutor_student_lists, 'New to Match and Learn? Sign up now!')
        self.assertTemplateUsed(respone_personal_profile, 'registration/login.html')