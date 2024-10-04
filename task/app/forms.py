from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm, AuthenticationForm
from .models import CustomUser,Class, Lesson, Question,Choice
import re
from django.forms import BaseInlineFormSet,inlineformset_factory

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(label='Username',max_length=55,widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    email = forms.EmailField(label='Email',widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    password1 = forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    password2 = forms.CharField(label='Confirm Password',widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}))
    role = forms.ChoiceField(choices=CustomUser.Role_choices,label='Role',widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'role')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(None)  
        if commit:
            user.save()
        return user

    error_messages = {
        'username': {
            'required': "Please enter a username.",
            'unique': "This username is already taken. Please choose another."
        },
        'email': {
            'required': "Please enter an email address.",
            'unique': "This email is already registered."
        },
        'password1': {
            'required': "Please enter a password.",
        },
        'password2': {
            'required': "Please confirm your password.",
            'password_mismatch': "The two passwords do not match."
        }
    }

class CustomUserChangeForm(UserChangeForm):
    username = forms.CharField(label='Username',max_length=55,widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    email = forms.EmailField(label='Email',widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    role = forms.ChoiceField(choices=CustomUser.Role_choices,label='Role',widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'role',)
        
    # def clean_username(self):
    #     username = self.cleaned_data.get('username')
    #     if not re.match(r'^[\w.@+-]+$', username):
    #         raise forms.ValidationError(
    #             "Enter a valid username. This value may contain only letters, numbers, and @/./+/-/_ characters."
    #         )
    #     return username

class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label='Old Password',widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password1 = forms.CharField(label='New Password',widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password2 = forms.CharField(label='Confirm New Password',widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = CustomUser
        fields = ['old_password', 'new_password1', 'new_password2']

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(label='Username',widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'class': 'form-control'}))





class ClassForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = ['name']

class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['lesson', 'class_name']
        
class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['text', 'is_correct']

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text', 'question_type', 'lesson', 'correct_answer']
        widgets = {
            
            'text':             forms.TextInput(attrs={     'class': 'form-control',        'placeholder': 'Question'}),
            
            'question_type':    forms.Select(attrs={        'class': 'form-control'                                    }),
            
            'lesson':           forms.Select(attrs={        'class': 'form-control'                                    }),
            
            'correct_answer':   forms.TextInput(attrs={     'class': 'form-control',        'placeholder': 'Correct Answer'}),
        }

class BaseChoiceFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        correct_choices = 0
        for form in self.forms:
            if not form.cleaned_data.get('DELETE',False):
                if form.cleaned_data.get('is_correct'):
                    correct_choices += 1
                if form.cleaned_data.get('text') == '' and form.cleaned_data.get('is_correct') is False:
                    continue
                if form.cleaned_data.get('text') == '' and form.cleaned_data.get('is_correct'):
                    raise forms.ValidationError('correct choice cant be empty.')
                
        if correct_choices != 1:
            raise forms.ValidationError('Exactly one choice must be marked as correct.')
    
ChoiceFormSet = inlineformset_factory(Question, Choice, form=ChoiceForm,    fields=('text','is_correct'), extra=10,min_num=2,max_num=4,validate_max=True,validate_min=True,formset=BaseChoiceFormSet)


class AssignStudentsForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(AssignStudentsForm, self).__init__(*args, **kwargs)
        self.fields['students'].queryset = CustomUser.objects.filter(role='student')
        print(self.fields['students'].queryset)  

    students = forms.ModelMultipleChoiceField(queryset=CustomUser.objects.filter(role='student'),widget=forms.CheckboxSelectMultiple,required=True)
