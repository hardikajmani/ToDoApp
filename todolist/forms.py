from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    #first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    #last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )
        #fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )


class ExportForm(forms.Form):
    email   = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    message = forms.CharField(max_length=1024, required=False, help_text='Optional') 

    class Meta:
        fields = ('email', 'message')