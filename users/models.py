from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone
from school.models import *
from datetime import date
import random


class CustomUserManager(BaseUserManager):
    """
    custom user model
    """

    def create_user(self, password=None, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        username = str(date.today().year) + 's' + str(CustomUser.objects.last().id + 1)
        possible_characters = "abcdefghijklmnopqrstuvwxyz1234567890"
        random_password = ''.join([random.choice(possible_characters) for i in range(8)])
        user = self.model(
            username=username,
            **extra_fields
        )

        user.set_password(random_password)
        user.save(using=self._db)
        return [user, random_password]

    def create_superuser(self, username, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.model(username=username, first_name='admin', surname='admin',
                          middle_name='admin', date_of_birth=date.today(), is_superuser=True, is_staff=True)
        user.set_password(password)
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):

    username = models.CharField(max_length=10, unique=True)
    email = models.EmailField(null=True)
    first_name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30)
    date_of_birth = models.DateField()
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    images = models.ManyToManyField('Image')
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):

        return '{0} {1} {2}'.format(self.first_name, self.surname, self.middle_name)


class Student(models.Model):

    user = models.OneToOneField('CustomUser', on_delete=models.CASCADE, primary_key=True)
    classroom = models.ForeignKey('school.Classroom', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.user.first_name + ' ' + self.user.surname + ' ' + self.user.middle_name


class Parent(models.Model):

    user = models.OneToOneField('CustomUser', on_delete=models.CASCADE, primary_key=True)
    student = models.ManyToManyField('Student')

    def __str__(self):
        return self.user.first_name + ' ' + self.user.surname + ' ' + self.user.middle_name


class Teacher(models.Model):

    user = models.OneToOneField('CustomUser', on_delete=models.CASCADE, primary_key=True)
    classroom = models.OneToOneField('school.Classroom', on_delete=models.SET_NULL, null=True, blank=True)
    is_head_teacher = models.BooleanField(default=False)

    def __str__(self):
        return self.user.first_name + ' ' + self.user.surname + ' ' + self.user.middle_name


class Image(models.Model):
    image = models.ImageField(upload_to='images/')
