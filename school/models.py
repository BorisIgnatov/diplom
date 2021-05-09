from django.db import models
from users.models import *


class Classroom(models.Model):

    title = models.CharField(max_length=10)

    def __str__(self):
        return self.title


class Subject(models.Model):

    teacher = models.ForeignKey('users.Teacher', on_delete=models.CASCADE)
    title = models.CharField(max_length=30)


class Schedule(models.Model):

    days = [
        ('MD', 'Monday'),
        ('TD', 'Tuesday'),
        ('WD', 'Wednesday'),
        ('THR', 'Thursday'),
        ('FRD', 'Friday'),
        ('STD', 'Saturday'),
        ('SD', 'Sunday')
    ]

    subject = models.ForeignKey('Subject', on_delete=models.CASCADE)
    classroom = models.ForeignKey('Classroom', on_delete=models.CASCADE)
    day_of_the_week = models.CharField(max_length=20, choices=days)
    time = models.TimeField()


class Quarter(models.Model):

    subject = models.ForeignKey('Subject', on_delete=models.CASCADE)
    student = models.ForeignKey('users.Student', on_delete=models.CASCADE)
    grade = models.IntegerField()


grades = [
        (0, 'n'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5')
    ]


class ClassWork(models.Model):

    subject = models.ForeignKey('Subject', on_delete=models.CASCADE)
    quarter = models.ForeignKey('Quarter', on_delete=models.CASCADE)
    grade = models.IntegerField(choices=grades)
    date = models.DateTimeField()
    description = models.CharField(max_length=50)


class HomeTask(models.Model):

    classroom = models.ForeignKey('Classroom', on_delete=models.CASCADE)
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE)
    teacher = models.ForeignKey('users.Teacher', on_delete=models.CASCADE)
    deadline = models.DateTimeField()
    title = models.CharField(max_length=30)
    description = models.TextField()


class HomeWork(models.Model):

    subject = models.ForeignKey('Subject', on_delete=models.CASCADE)
    quarter = models.ForeignKey('Quarter', on_delete=models.CASCADE)
    student = models.ForeignKey('users.Student', on_delete=models.CASCADE)
    grade = models.IntegerField(choices=grades)
    date = models.DateTimeField()
    description = models.CharField(max_length=50)
    attachment = models.ManyToManyField('HomeWorkAttachment')


class HomeWorkAttachment(models.Model):

    file = models.FileField(upload_to='homeworkFiles')


class QuizTask(models.Model):

    classroom = models.ForeignKey('Classroom', on_delete=models.CASCADE)
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE)
    teacher = models.ForeignKey('users.Teacher', on_delete=models.CASCADE)
    deadline = models.DateTimeField()
    start_time = models.DateTimeField()
    title = models.CharField(max_length=30)
    description = models.TextField()


#TODO create quiz question and choices and exam


class Quiz(models.Model):

    subject = models.ForeignKey('Subject', on_delete=models.CASCADE)
    quarter = models.ForeignKey('Quarter', on_delete=models.CASCADE)
    grade = models.IntegerField(choices=grades)
    date = models.DateTimeField()
    description = models.CharField(max_length=50)


class Exam(models.Model):

    subject = models.ForeignKey('Subject', on_delete=models.CASCADE)
    quarter = models.ForeignKey('Quarter', on_delete=models.CASCADE)
    grade = models.IntegerField(choices=grades)
    date = models.DateTimeField()
    description = models.CharField(max_length=50)


class Attendance(models.Model):

    subject = models.ForeignKey('Subject', on_delete=models.CASCADE)
    quarter = models.ForeignKey('Quarter', on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    is_here = models.BooleanField(default=False)
