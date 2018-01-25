from __future__ import unicode_literals
from django.db import models
import re
import bcrypt
from datetime import date
import datetime
import calendar


class UserManager(models.Manager):
    def register_validator(self, postData):

        results = {'status': True, 'errors': []}
        if len(postData['name'])==0:
            results["errors"].append("'Name' is a required field.")
        if len(postData['name'])<3:
            results["errors"].append("Name should be more than 2 characters.")
        if not re.match('[a-zA-Z]{2,}\s?[a-zA-z]{1,}?', postData['name']):
            results["errors"].append("Names must be characters (a-z) only.")
        if len(postData['email'])==0:
            results["errors"].append("'Email' is a required field.")
        if not re.match('(\w+[.|\w])*@(\w+[.])*\w+', postData['email']):
            results["errors"].append("Please enter a valid email.")
        if len(postData['psw'])<8:
            results["errors"].append("Passwords must be at least 8 characters long.")
        if postData['psw'] != postData['cfm']:
            results["errors"].append("Passwords do not match.")

        #TODO name && email must be unique
        
        try:
            dobstr = postData['birthdate']
            dob = datetime.datetime.strptime(dobstr, "%Y-%m-%d").date()
            if dob > date.today():
                results['errors'].append('Birthdate must be before today.')
        except:
            results["errors"].append("'Birthdate' is a required field.")

            
        if len(results['errors']):
            results['status']=False
        # print results
        return results

    def createUser(self, postData):
        hash1 = bcrypt.hashpw(postData['psw'].encode(), bcrypt.gensalt())
        user = User.objects.create(
            name=postData['name'],
            email=postData['email'],
            password=hash1,
            birthdate=postData['birthdate']
        )
        return user

    def login_validator(self, postData):
        results = {'status': True, 'errors': [], 'user': None}
        # filter for email in db
        users = self.filter(email = postData['email'])
        if len(users) < 1:
            results['errors'].append("User not found.")
        elif bcrypt.checkpw(postData['psw'].encode(), users[0].password.encode())==False:
            results["errors"].append("Password is incorrect.")
        
        if len(results['errors']):
            results['status']=False
        else:
            results['user']=users[0]
        return results

class User(models.Model):
    name = models.CharField(max_length=50) 
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    birthdate = models.DateField(auto_now_add=False)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()
    def __str__(self):
        return "<User object: {} {}>".format(self.id, self.alias)


