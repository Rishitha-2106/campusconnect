from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'year', 'department', 'password1', 'password2']
    def clean_email(self):
        email = self.cleaned_data.get('email')
        allowed_domain = "svecw.edu.in"
        if not email.endswith(f"@{allowed_domain}"):
            raise forms.ValidationError(f"Please register using your college email address ending with @{allowed_domain}.")
        return email