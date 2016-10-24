from __future__ import unicode_literals
from django.db import models
import bcrypt
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

#managers
class UserManager(models.Manager):
    def validation(self, email, password, conf_password, first_name, last_name, username):
        fields=[]
        if not EMAIL_REGEX.match(email):
            print ("Email NOT valid")
            fields.append("Email invalid")
        if len(first_name) < 3:
            print ('first name must be entered')
            fields.append('first name must be entered')
        if len(last_name) < 3:
            print ('last name must be entered')
            fields.append('last name must be entered')
        if len(username) < 3:
            print ('Username must be entered')
            fields.append('Username must be entered')
        if len(password) < 8:
            print ('password must be at least 8 characters')
            fields.append('password must be at least 8 characters')
        if password != conf_password:
            print ('Make sure password confirmation matches')
            fields.append('Make sure password confirmation matches')
        if fields:
            return fields

    def login(self, username, entered_pw):
            l_fields=[]
            print "at login"
            try:
                user = Users.objects.get(username=username)#select * from users where #email = email
                print user
                if user.pw_hash == bcrypt.hashpw(entered_pw.encode(), user.pw_hash.encode()):
                    l_fields.append("success!")
                    print ('password match confirmed')
                    return user
                else:
                    l_fields.append("Incorrect password")
            except:
                l_fields.append("Email does not match our records")
            return l_fields


#models
class Users(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    username = models.CharField(max_length=45)
    pw_hash=models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    hired = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects=UserManager()

class Items(models.Model):
    user = models.ForeignKey(Users)
    product = models.CharField(max_length=255)
    add_date = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Wishlists(models.Model):
    item = models.ForeignKey(Items)
    user = models.ForeignKey(Users)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
