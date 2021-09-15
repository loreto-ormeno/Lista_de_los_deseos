from django.db import models
from datetime import date, datetime
import re

# Create your models here.

class UserManager(models.Manager):
    def validador_campos(self, postData):
        JUST_LETTERS = re.compile(r'^[a-zA-Z.]+$')
        JUST_LETTERS_NUMBER = re.compile(r'^(?=\w*\d)(?=\w*[A-Z])(?=\w*[a-z])\S{3,50}$')
        PASSWORD_REGEX = re.compile(r'^(?=\w*\d)(?=\w*[A-Z])(?=\w*[a-z])\S{8,16}$')

        errors = {}

        if len(User.objects.filter(username=postData['username'])) > 0:
            errors['username_exits'] = "Usuario ya existe!!!"
        
        else:
            if len(postData['name'].strip()) < 3 or len(postData['name'].strip()) > 50:
                errors['name_len'] = "Nombre debe tener entre 3 y 50 caracteres"

            if len(postData['username'].strip()) < 3 or len(postData['username'].strip()) > 50:
                errors['username_len'] = "Usuario debe tener entre 3 y 50 caracteres sin espacios"

            #if not JUST_LETTERS_NUMBER.match(postData['username']):
            #    errors['just_letters_number'] = "Username debe tener entre 3 y 50 caracteres sin espacios"
                        
            #if not JUST_LETTERS.match(postData['name']):
            #    errors['just_letters'] = "Solo se permite el ingreso de letras en el nombre y apellido"
                
            if not PASSWORD_REGEX.match(postData['password']):
                errors['password_format'] = "Formato contraseña no válido"

            if postData['password'] != postData['password_confirm']:
                errors['password_confirm'] = "Contraseñas no coinciden"

            now = date.today()
            doh = datetime.strptime(postData['datehired'],'%Y-%m-%d').date()
            delta_date = now - doh
            delta_days = delta_date.days

            if delta_days < 0:
                errors['doh_bad_date'] = 'La fecha de registro debe ser anterior'

        return errors


class ItemManager(models.Manager):
    def validador_item(self, postData):

        errors = {}

        if len(postData['item_create'].strip()) < 3 or len(postData['item_create'].strip()) > 50:
            errors['description_len'] = "Descripción debe tener mas de 3 caracteres"
     
        return errors


class User(models.Model):
    name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=250)
    datehired = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    
    def __str__(self):
        return self.name


class Item(models.Model):
    description = models.TextField(max_length=100)
    wisher = models.ManyToManyField(User, related_name="wisher_user", blank=True)
    creator = models.ForeignKey(User, related_name="user_creator", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ItemManager()
    
    def __str__(self):
      return self.description
