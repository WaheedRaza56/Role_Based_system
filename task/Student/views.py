from django.shortcuts import render, redirect,get_object_or_404
from .forms import *
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model,logout as auth_logout
from django.db import IntegrityError
from .models import *

from django.shortcuts import render
from .models import *

def student_dashboard(request):
    student_classes = Class.objects.filter(students=request.user)  
    student_lessons = Lesson.objects.filter(class_name__in=student_classes)

    lesson_quizzes = []
    for lesson in student_lessons:
        questions = lesson.questions.all()
        answered_questions = Answer.objects.filter(student=request.user, question__in=questions).values_list('question_id', flat=True)

        lesson_quizzes.append({'lesson': lesson,'questions': questions,'answered_questions': answered_questions,})

    context = {
        'lesson_quizzes': lesson_quizzes,
    }
    return render(request, 'student/student_dashboard.html', context)



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
                    return redirect('student:change_password')
                else:
                    return redirect('student:student_dashboard')
            else:
                print("Manual authentication failed")
                messages.error(request, 'Invalid username or password')
        else:
            print(f"User with username '{username}' does not exist")
            messages.error(request, 'Invalid username or password')
    else:
        form = CustomLoginForm()
    return render(request, 'student/login.html', {'form': form})


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
            return redirect('student:student_dashboard')  
    else:
        form = CustomPasswordChangeForm(request.user)
    return render(request, 'student/change_password.html', {'form': form})


def logout(request):
    if request.method == 'POST':
        user = request.user
        if user.is_authenticated:
            if user.role == 'student':
                print(f"Teacher {user.username} is logging out.")
            auth_logout(request)
            return redirect('student:login') 

    return redirect('student:student_dashboard') 




def quiz_view(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    questions = lesson.questions.all()

    processed_questions = []
    for question in questions:
        choices = question.choices.all() if question.question_type == 'MC' else []
        processed_questions.append({'question': question, 'choices': choices})

    if request.method == 'POST':
        score = 0
        for question in questions:
            answer_text = request.POST.get(f'question_{question.id}', '')
            is_correct = answer_text == question.correct_answer
            
            try:
                Answer.objects.create(student=request.user, question=question, answer=answer_text, is_correct=is_correct)
                if is_correct:
                    score += 1
            except IntegrityError as e:
                print(f"IntegrityError when saving answer: {e}")
                return render(request, 'student/quiz_result.html', {'score': score, 'lesson': lesson, 'error': 'Error recording answer. Please try again later.'})

        return render(request, 'student/quiz_result.html', {'score': score, 'lesson': lesson})

    return render(request, 'student/quiz.html', {'questions': processed_questions, 'lesson': lesson})




