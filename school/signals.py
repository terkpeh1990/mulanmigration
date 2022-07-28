from django.db.models.signals import post_save, pre_init
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.auth import user_logged_in
from django.dispatch.dispatcher import receiver
from django.contrib.auth.hashers import make_password
# from .models import Profile, UserSession
from django.shortcuts import redirect
import datetime
from .models import *
from django.contrib.sessions.models import Session
from .import views
from twilio.rest import TwilioRestClient
from twilio.rest import Client
from school_management_system.settings import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER
User = get_user_model()

def staff_profile(sender,instance,created,**kwargs):
    if created:
        ff ="password@12345"
        cc= User.objects.create(
            username= instance.id,
            password=make_password(ff),
            first_name = instance.firstname,
            last_name= instance.Surname
        )
        group = Group.objects.get(name='teacher')
        cc.groups.add(group)
        Profile.objects.create(
            user=cc,
            name = cc.first_name + " " + cc.last_name,
            email = cc.email,
            is_staff= True,
            is_new =True
        )
post_save.connect(staff_profile,sender=Staffs)


def parent_profile(sender, instance, created, **kwargs):
    if created:
        ff = "password@12345"
        cc = User.objects.create(
            username=instance.id,
            password=make_password(ff),
            first_name=instance.father_name,
            last_name=instance.mother_name
        )
        group = Group.objects.get(name='parent')
        cc.groups.add(group)
        Profile.objects.create(
            user=cc,
            name=cc.first_name + " " + cc.last_name,
            email=cc.email,
            is_parent=True,
            is_new=True
        )


post_save.connect(parent_profile, sender=Parents)


# def student_profile(sender, instance, created, **kwargs):
#     if created:
#         ff = "paswword@12345"
#         cc = User.objects.create(
#             username=instance.id,
#             password=make_password(ff),
#             first_name=instance.firstname,
#             last_name=instance.Surname
#         )
#         group = Group.objects.get(name='teacher')
#         cc.groups.add(group)
#         Profile.objects.create(
#             user=cc,
#             name=cc.first_name + " " + cc.last_name,
#             email=cc.email,
#             is_staff=True,
#             is_new=True
#         )


# post_save.connect(staff_profile, sender=Students)

# @receiver(user_logged_in)
# def remove_other_sessions(sender, user, request, **kwargs):
#     # remove other sessions
#     Session.objects.filter(usersession__user=user).delete()

#     # save current session
#     request.session.save()

#     # create a link from the user to the current session (for later removal)
#     UserSession.objects.get_or_create(
#         user=user,
#         session=Session.objects.get(pk=request.session.session_key)
#     )
#     return redirect('log')
