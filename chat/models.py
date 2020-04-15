from django.db import models

class Chatroom(models.Model):#create chat room model
    room_name = models.TextField(blank=True)#collect room name
    user1 = models.TextField(blank=True)
    user2 = models.TextField(blank=True)
    chat = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)#collect a time when you send
    def __str__(self):
        return self.room_name