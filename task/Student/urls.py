from django.urls import path
from . import views

app_name = 'student'

urlpatterns = [ 
    path('student/login/', views.login_view, name='login'),
    path('student/logout/', views.logout, name='logout'),
    path('student/change_password/', views.change_password, name='change_password'),
    path('student/student_dashboard/', views.student_dashboard, name='student_dashboard'),
    path('quiz/<int:lesson_id>/', views.quiz_view, name='quiz_view'),
]
