from __future__ import unicode_literals
from django.db import models
from django.contrib import messages
import re
import bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def validations(self,postData):
        errors = {} 
        if len(postData["first"]) < 1:
            errors["firsterror"] = "Name cannot be blank."
        elif not postData['first'].isalpha() :
            errors['firsterror'] = "Name can only contain letters."
        if len(postData['last']) < 1:
            errors['lasterror'] = "Last Name cannot be blank."
        elif not postData['last'].isalpha():
            errors['lasterror'] = "Last name can only contain letters."
        if len(postData['email']) < 1:
            errors['emailerror'] = "Email required"
        elif not EMAIL_REGEX.match(postData['email']):
            errors['emailerror'] = "Email invalid"
        if len(postData['pass1']) < 1:
            errors['passerror'] = "Password missing."
        if postData['pass2'] != postData['pass1']:
            errors['passerror'] = "Passwords didn't match!"
        if User.objects.filter(email=postData['email']).count() > 0:
            errors['email'] = "Email already exists"
        print(postData)
        return errors

    def login(self,postData):
        errors2 ={}
        if len(postData['email']) < 1:
            errors2['email'] = "Missing required fields Email/Password"
        elif not EMAIL_REGEX.match(postData['email']):
            errors2['email'] = "Invalid Email"
        elif User.objects.filter(email=postData['email']).count() == 0:
            errors2['email'] = " Email doesn't exist"
        if len(postData['pass1']) < 1:
            errors2['pass1'] = "Password cannot be blank"
        # elif User.objects.filter(passhash=postData['pass1']).count() == 0:
        #     errors2['pass1'] = "Failed to login Email/Password"
        print(postData)
        return errors2


class User(models.Model):
    first_name= models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    passhash = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()



