from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class CustomUser(AbstractUser):
    Role_choices = (
        ('teacher', 'Teachers'),
        ('student', 'Students'),
    )
    role = models.CharField(max_length=10, choices=Role_choices, default='teacher')
    has_changed_password = models.BooleanField(default=False)
    
    groups = models.ManyToManyField(Group,related_name='customuser_set', blank=True,help_text='A user will get all permissions granted to each of their groups.',verbose_name='groups',)
    user_permissions = models.ManyToManyField(Permission,related_name='customuser_set',blank=True,help_text='Specific permissions for this user.',verbose_name='user permissions',)

    def __str__(self):
        return self.username

class Teachers(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=False)

class Students(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=False)



class Class(models.Model):
    name = models.CharField(max_length=100)
    teacher = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='classes')
    students = models.ManyToManyField(CustomUser, related_name='classes_as_student', blank=True)

    def __str__(self):
        return self.name


class Lesson(models.Model):
    lesson = models.CharField(max_length=100)
    class_name = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='lessons')
    teacher = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='lessons') 

    def __str__(self):
        return self.lesson
    
class Question(models.Model):
    QUESTION_TYPES = [
        ('FB', 'Fill in the blanks'),
        ('TF', 'True/False'),
        ('MC', 'Multiple Choice'),
    ]
    text = models.TextField()
    question_type = models.CharField(max_length=2, choices=QUESTION_TYPES)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='questions')
    correct_answer = models.TextField()

    def __str__(self):
        return self.text
    


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text



class Answer(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    answer = models.TextField()
    is_correct = models.BooleanField()


    def __str__(self):
        return f"{self.student.username} - {self.question.text} - {self.is_correct}"
