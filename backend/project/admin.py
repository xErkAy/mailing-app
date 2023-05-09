from django.contrib import admin
from project.models import User
from mailing.models import Client, Mail, Message

admin.site.register(User)
admin.site.register(Client)
admin.site.register(Mail)
admin.site.register(Message)