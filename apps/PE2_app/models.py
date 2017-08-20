from __future__ import unicode_literals
from django.db import models
import re, bcrypt
import datetime
# Create your models here.
USERNAME_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+$')


class UserManager(models.Manager):
    def registration_validator(self, postData):
        errors = {}
        if len(postData['name']) < 3: #or not postData['first_name'].isalpha():
            errors['name'] = "Input a name longer than 2 Characters"

        if len(postData['username']) < 3: # or not postData['first_name'].isalpha():
            errors['username'] = "Enter an username"

        if len(postData['password']) < 8:
            errors['password'] = "Password must be 8 characters minimum"

        if postData['password'] != postData['confirm']:
            errors['confirm'] = "Passwords do not match!"

        if not USERNAME_REGEX.match(postData['username']):
            errors['pass'] = "Invalid username address"

        if len(postData['datehired']) < 1:
            errors['datehired'] = "Enter the date hired!"

        if postData['datehired']: #if no date input is made, these dont run
            hired = datetime.datetime.strptime(postData['datehired'], "%Y-%m-%d")
            today = datetime.date.today() #format given '2008-11-22 19:53:42'
            today = datetime.datetime(today.year, today.month, today.day) #changes it to '2008-11-22'

            if hired > today:
                errors['dateErr'] = "We do not associate with people from the future!"

        try:
            User.objects.get(username = postData['username']) #doesnt allow duplicate usernames
            errors['duplicate'] = "username already registered"

        except:
            pass


        if len(errors):
            return errors


        hashed_pw = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())

        user = User.objects.create(
            name = postData['name'],
            username = postData['username'],
            password = hashed_pw,
            datehired = postData['datehired']
            )
        return user.id


    def login_validator(self, postData):
            errors ={}

            if len(postData['username']) < 1:
                errors['login_username'] = "Enter an username"

            try:
                user = User.objects.get(username = postData['username'])
                if not bcrypt.checkpw(postData['password'].encode(), user.password.encode()):
                    errors['login_pass'] = "Incorrect Username/Password!"

            except:
                errors['login_val'] = "Login info incorrect!"

            if errors:
                return errors

            else:
                return user.id



class ItemManager(models.Manager):
    def item_validation(self, postData, uid):
        errors = {}
        print "#" * 50
        if len(postData['name']) < 3:
            errors['destination'] = "Enter item name!"

        if errors: # if there are errors it will return them, else the plan will be created
            return errors

        item = Item.objects.create(
            name = postData['name'],
            users = User.objects.get(id = uid),
        )
        # newid = Item.objects.filter(all_users__id = uid)
        # print(newid)
        # Item.objects.filter(all_users__id = uid)
        return item.id

    def join_validation(self, postData, iid, uid):
        user1 = User.objects.get(id=uid) #put into a variable to insert whole object into many_users
        add = Item.objects.get(id=iid).all_users.add(user1) #many to many query. Gets the plan by id and adds user1 (object) to 'many_users'
        return add

    def remove_validation(self, postData, iid, uid):
        # user = User.objects.get(id=uid)
        # remove = Item.objects.get(all_users = user).delete()
        # return remove
        pass

class User(models.Model):
    name = models.CharField(max_length = 100)
    username = models.CharField(max_length = 100)
    password = models.CharField(max_length = 100)
    datehired = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager() #links UserManager class


class Item(models.Model):
    name = models.CharField(max_length=255)
    users = models.ForeignKey(User, related_name='items')
    # One-to-many == user can plan many trips, a trip can only have one planner
    all_users = models.ManyToManyField(User, related_name = "all_items")
    # Many-to-many == Users can have many trips, trips can have many users
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ItemManager()
