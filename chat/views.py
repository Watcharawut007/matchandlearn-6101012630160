# chat/views.py
from django.shortcuts import render
from .models import Chatroom
from django import db
from django.db import close_old_connections
from tinderforeduapp.models import  *

def room(request, roomname):#this fucntion used when user join in chat room
    splitlog = [] #Collect all message in this room
    log = ""#Collect all message in string form
    user = roomname.split("_")
    usercheck1 = user[0]
    usercheck2 = user[1]
    username = request.user.username
    if Chatroom.objects.filter(room_name=roomname, user1=usercheck1, user2=usercheck2).exists():
        if (Chatroom.objects.get(room_name=roomname).user1 == username) or (Chatroom.objects.get(room_name=roomname).user2 == username):
            log = Chatroom.objects.get(room_name=roomname).chat
            splitlog = log.split("`~`~`~`~`~`")#split with "`~`~`~`~`~`" for know that are message
            usercheck1 = Chatroom.objects.get(room_name=roomname).user1#check that user can read chat room
            usercheck2 = Chatroom.objects.get(room_name =roomname).user2#check that user can read chat room

    return render(request, 'chat/room.html', {'user_information':UserInfo.objects.get(name=request.user.username),
                                              'room_name': roomname,
                                              'log': log,
                                              'usercheck1': usercheck1,
                                              'usercheck2': usercheck2,
                                              'splitlog': splitlog})

