from django import forms
from .models import Room
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['name', 'tag', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control bg-transparent text-light'}),
            'tag': forms.Select(attrs={'class': 'form-control bg-transparent text-light'}),
            'description': forms.Textarea(attrs={'class': 'form-control bg-transparent text-light'}),
        }

class SignupForm(UserCreationForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control bg-transparent text-light'}),
    )
    password2 = forms.CharField(
        label="Confirm password",
        widget=forms.PasswordInput(attrs={'class': 'form-control bg-transparent text-light'}),
    )
    
    class Meta:
         model = User
         fields = ['name', 'username', 'email', 'university', 'password1', 'password2']

         widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control bg-transparent text-light'}),
            'username': forms.TextInput(attrs={'class': 'form-control bg-transparent text-light'}),
            'email': forms.EmailInput(attrs={'class': 'form-control bg-transparent text-light'}),
            'university': forms.Select(attrs={'class': 'form-control bg-transparent text-light'}),
        }

class UpdateProfileForm(forms.ModelForm):
    class Meta:
         model = User
         fields = ['name', 'username', 'email', 'university', 'image']

         widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control bg-transparent text-light'}),
            'username': forms.TextInput(attrs={'class': 'form-control bg-transparent text-light'}),
            'email': forms.EmailInput(attrs={'class': 'form-control bg-transparent text-light'}),
            'university': forms.Select(attrs={'class': 'form-control bg-transparent text-light'}),
            # 'image': forms.FileInput(attrs={'class': 'form-control bg-transparent text-light'})
        }