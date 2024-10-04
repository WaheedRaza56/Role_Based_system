from django.shortcuts import render, redirect,get_object_or_404
from .forms import *
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model,logout as auth_logout
from .models import *

# Create your views here.


def teacher_dashboard(request):
    classes = Class.objects.filter(teacher=request.user)
    return render(request, 'teacher/teacher_dashboard.html', {'classes': classes})


def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        User = get_user_model()
        user_exists = User.objects.filter(username=username).exists()
        print(f"User '{username}' exists: {user_exists}")
        
        if user_exists:
            authenticated_user = authenticate(username=username, password=password)
            if authenticated_user is not None:
                print("Manual authentication successful")
                login(request, authenticated_user)
                if not authenticated_user.has_changed_password:
                    return redirect('teacher:change_password')  
                else:
                    return redirect('teacher:teacher_dashboard')
            else:
                print("Manual authentication failed")
                messages.error(request, 'Invalid username or password')
        else:
            print(f"User with username '{username}' does not exist")
            messages.error(request, 'Invalid username or password')
    else:
        form = CustomLoginForm()
    return render(request, 'teacher/login.html', {'form': form})


@login_required
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            user.has_changed_password = True
            user.save()
            messages.success(request, 'Your password was successfully updated!')
            return redirect('teacher:teacher_dashboard')  
    else:
        form = CustomPasswordChangeForm(request.user)
    return render(request, 'teacher/change_password.html', {'form': form})

def logout(request):
    if request.method == 'POST':
        user = request.user
        if user.is_authenticated:
            if user.role == 'teacher':
                print(f"Teacher {user.username} is logging out.")
            auth_logout(request)
            return redirect('teacher:login') 

    return redirect('teacher:teacher_dashboard') 
    
    
def create_class(request):
    if request.method == 'POST':
        form = ClassForm(request.POST)
        if form.is_valid():
            class_form = form.save(commit=False)
            class_form.teacher = request.user
            class_form.save()
            return redirect("teacher:teacher_dashboard")
        else:
            print(form.errors)
    else:
        form = ClassForm()
    return  render(request,'teacher/create_class.html',{'form':form})



def create_lesson(request):
    if request.method == 'POST':
        form = LessonForm(request.POST)
        if form.is_valid():
            new_lesson = form.save(commit=False)
            new_lesson.teacher = request.user 
            new_lesson.save()
            return redirect('teacher:teacher_dashboard')
    else:
        form = LessonForm()    
    return render(request, 'teacher/create_lesson.html', {'form': form})


def create_question(request):   
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        formset = ChoiceFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            question = form.save()
            choices = formset.save(commit=False)
            for choice in choices:
                if choice.text:
                    choice.question = question
                    choice.save()
    else:
        form = QuestionForm()
        formset = ChoiceFormSet()
    return render(request, 'teacher/create_question.html', {'form': form, 'formset': formset})



def assign_student(request, id):
    class_instance = get_object_or_404(Class, id=id)
    if request.method == 'POST':
        form = AssignStudentsForm(request.POST)
        if form.is_valid():
            students = form.cleaned_data['students']
            class_instance.students.set(students)
            return redirect('teacher:teacher_dashboard')
    else:
        form = AssignStudentsForm()

    return render(request, 'teacher/assign_students.html', {'form': form, 'class_instance': class_instance})
