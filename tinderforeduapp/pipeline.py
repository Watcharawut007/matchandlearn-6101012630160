from .models import UserInfo, Profilepicture
from django.contrib.auth.models import User
from social_core.pipeline.user import get_username as social_get_username
from datetime import date, datetime
user_email = ""

def get_email(backend, user, response, *args, **kwargs):#get email
    global user_email

    if response.get('email') == None:
        user_email = (response.get('url_room_name')).split(" ")[0] + (response.get('url_room_name')).split(" ")[1]

    else:
        user_email = (response.get('email')).split("@")[0]

def user_profile_db(backend, user, response, *args, **kwargs):#create a model userinfo when signup with facebook

    if not User.objects.filter(email=response.get('email')).exists():
        gender = ''
        birthdate = response.get('birthday')#get birthday
        born = datetime.strptime(birthdate, '%m/%d/%Y')
        age = int((datetime.today() - born).days/365)#calculate age

        if response.get('gender') == 'male':
            gender = 'Male'

        if response.get('gender') == 'female':
            gender = 'Female'

        if response.get('email') == None:
            user = UserInfo.objects.create(name=(response.get('url_room_name')).split(" ")[0] + (response.get('url_room_name')).split(" ")[1],
                                           school='',
                                           age=age,
                                           fullname=(response.get('url_room_name')).split(" ")[0],
                                           lastname=(response.get('url_room_name')).split(" ")[1],
                                           gender=gender, fb_link=response.get('link'))

        else:
            user = UserInfo.objects.create(name=(response.get('email')).split("@")[0],
                                           school='',
                                           age=age,
                                           fullname=(response.get('url_room_name')).split(" ")[0],
                                           lastname=(response.get('url_room_name')).split(" ")[1],
                                           gender=gender, fb_link=response.get('link'))
        Profilepicture.objects.create(user=user, images='default.png')


def get_username(strategy, details, backend, user=None, *args, **kwargs):#get a username
    result = social_get_username(strategy, details, backend, user=user, *args, **kwargs)
    result['username'] = user_email
    return result