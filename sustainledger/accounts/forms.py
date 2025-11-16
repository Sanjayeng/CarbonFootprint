from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm

class RegisterForm(forms.ModelForm):
   password = forms.CharField(widget=forms.PasswordInput)
   password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)
   class Meta:
    model = User
    fields = ('username', 'email', 'password')


def clean_password2(self):
  p1 = self.cleaned_data.get('password')
  p2 = self.cleaned_data.get('password2')
  if p1 and p2 and p1 != p2:
   raise forms.ValidationError("Passwords don't match")
  return p2


class LoginForm(AuthenticationForm):
# you can customize placeholders or classes here
 pass