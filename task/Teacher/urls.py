from django.urls import path
from . import views

app_name = 'teacher'

urlpatterns = [
    path('teacher/login/', views.login_view, name='login'),
    path('teacher/logout/', views.logout, name='logout'),
    path('teacher/change_password/', views.change_password, name='change_password'),
    path('teacher/teacher_dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    
    path('teacher/create_class/', views.create_class, name='create_class'),
    path('teacher/create_lesson/', views.create_lesson, name='create_lesson'),
    path('teacher/create_question/', views.create_question, name='create_question'),
    path('teacher/assign_student/<int:id>/', views.assign_student, name='assign_student'),
    

]
