# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.conf import settings
from .forms import CustomUserCreationForm, CustomUserChangeForm,PasswordChangeForm
from .models import CustomUser, Teachers, Students
from django.contrib.auth.hashers import make_password ,check_password
from .mathing import generate_random_password 
from django.contrib.auth import update_session_auth_hash


#################################################   admin_dashboard   ##############################################

def admin_dashboard(request):
    users = CustomUser.objects.all()
    return render(request, 'adminpanel/dashboard.html', {'users': users})

#################################################   create_user   ##################################################

print(generate_random_password)
# def create_user(request):
#     if request.method == 'POST':
#         form = CustomUserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             if CustomUser.objects.filter(username=user.username).exists():
#                 messages.error(request, 'Username already exists.')
#                 return redirect('adminpanel:admin_dashboard')
#             if user.role == 'teacher':
#                 random_password = generate_random_password(length=12)
#                 print(f"Generated Password: {random_password}") 
#                 user.set_password(random_password)
#                 user.save()
                
#                 print(f"Hashed password in the database: {user.password}")
#                 Teachers.objects.get_or_create(user=user)
                
#                 subject = 'Account Information'
#                 message = f'Your {user.username} account has been created. Your temporary password is: {random_password}. Please change it on your first login.'
#                 send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
                
#             elif user.role == 'student':
#                 user.save()
#                 Students.objects.get_or_create(user=user)
            
#             messages.success(request, 'User created successfully!')
#             return redirect('adminpanel:admin_dashboard')
#         else:
#             messages.error(request, 'Please correct the errors below.')
#     else:
#         form = CustomUserCreationForm()
#     return render(request, 'adminpanel/create_user.html', {'form': form})




def create_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            if CustomUser.objects.filter(username=user.username).exists():
                messages.error(request, 'Username already exists.')
                return redirect('adminpanel:admin_dashboard')

            random_password = generate_random_password(length=12)
            print(f"Generated Password: {random_password}") 
            user.set_password(random_password)
            user.save()
            
            print(f"Hashed password in the database: {user.password}")

            if user.role == 'teacher':
                Teachers.objects.get_or_create(user=user)
            elif user.role == 'student':
                Students.objects.get_or_create(user=user)
            
            subject = 'Account Information'
            message = f'Your {user.username} account has been created. Your temporary password is: {random_password}. Please change it on your first login.'
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
            
            messages.success(request, 'User created successfully!')
            return redirect('adminpanel:admin_dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'adminpanel/create_user.html', {'form': form})



#################################################   update_user   ##################################################


def update_user(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=user)
        print("Submitted data:", request.POST)
        if form.is_valid():
            print("after valid")
            user = form.save(commit=False)
            if 'role' in form.changed_data:
                if user.role == 'teacher':
                    Teachers.objects.get_or_create(user=user)
                    Students.objects.filter(user=user).delete()
                elif user.role == 'student':
                    Students.objects.get_or_create(user=user)
                    Teachers.objects.filter(user=user).delete()
            user.save()
            messages.success(request, 'User updated successfully!')
            return redirect('adminpanel:admin_dashboard')
        else:
            print("Form errors:", form.errors)  
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomUserChangeForm(instance=user)
    return render(request, 'adminpanel/update_user.html', {'form': form, 'user': user})


def delete_user(request,pk):
    user = get_object_or_404(CustomUser,pk=pk)
    user.delete()
    return redirect('adminpanel:admin_dashboard')

