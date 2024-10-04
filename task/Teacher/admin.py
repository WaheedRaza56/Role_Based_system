from django.contrib import admin
from .models import  Class, Lesson, Question
# Register your models here.



@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ['name', 'teacher']
    search_fields = ['name', 'teacher__username']
    

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['lesson', 'class_name']
    search_fields = ['lesson', 'class_name__name']
    

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['text', 'lesson','question_type','correct_answer']
    search_fields = ['text', 'lesson__title']