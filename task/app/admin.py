from django.contrib import admin
from .models import CustomUser, Teachers, Students
from django.contrib.auth.admin import UserAdmin
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.conf import settings


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'is_active', 'is_staff')
    search_fields = ('username', 'email')
    list_filter = ('role',)
    
    fieldsets = (
        (None,              {'fields':      ('username', 'password')}),
        
        ('Personal info',   {'fields':      ('first_name', 'last_name', 'email')}),
        
        ('Permissions',     {'fields':      ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        
        ('Important dates', {'fields':      ('last_login',)}),
        
        ('Role',            {'fields':      ('role',)}),
    )
    
    # def save_model(self, request, obj, form, change):
    #     if not change:
    #         if obj.role == 'teacher':
    #             password = get_random_string(length=8)
    #             obj.set_password(password)
    #             obj.save()
                
    #             Teachers.objects.get_or_create(user=obj)
    #             subject = 'Account Information'
    #             message = f'Account has been created. Your temporary password is: {password}. Please change it on your first login.'
                
    #             try:
    #                 send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [obj.email])
    #                 self.message_user(request, "Email sent successfully.")
    #             except Exception as e:
    #                 self.message_user(request, f"Error sending email: {e}", level='error')
    #     else:
    #         if 'role' in form.changed_data:
    #             if obj.role == 'teacher':
    #                 Teachers.objects.get_or_create(user=obj)
    #                 Students.objects.filter(user=obj).delete()
    #             elif obj.role == 'student':
    #                 Students.objects.get_or_create(user=obj)
    #                 Teachers.objects.filter(user=obj).delete()
    #     super().save_model(request, obj, form, change)

@admin.register(Teachers)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user__username', 'user_email')
    
@admin.register(Students)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user__username',)

admin.site.register(CustomUser, CustomUserAdmin)
