from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
class myUserCreationForm(UserCreationForm):
    username = forms.CharField(widget = forms.TextInput(attrs={
        'label' : 'Username',
        'class': "form-control",
        'id' : "usernametextinput",
        'type' : 'text',
        'placeholder' : "Enter username"
        }))
    password1 = forms.CharField(widget = forms.TextInput(attrs={
        'class': "form-control",
        'id' : "floatingpasswordinput1",
        'type' : 'password',
        'placeholder' : "Enter your password"
        }))
    password2 = forms.CharField(widget = forms.TextInput(attrs={
        'label' : "Confirm Password ",
        'class': "form-control",
        'id' : "floatingpasswordinput2",
        'type' : 'password',
        'placeholder' : "Confirm your password"
        }))
    class Meta:
        model=User
        fields = ('username', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super(myUserCreationForm, self).__init__(*args, **kwargs)
        
class UserChangePasswordForm(UserCreationForm):
    username = forms.CharField(widget = forms.TextInput(attrs={
        'label' : 'Username',
        'class': "form-control",
        'id' : "usernametextinput",
        'type' : 'text',
        'placeholder' : "Enter username"
        }))
    currentpassowrd = forms.CharField(widget = forms.TextInput(attrs={
        'class': "form-control",
        'id' : "floatingpasswordinput1",
        'type' : 'password',
        'placeholder' : "Enter your current password"
        }))
    newrepeatpassword = forms.CharField(widget = forms.TextInput(attrs={
        'class': "form-control",
        'id' : "floatingpasswordinput1",
        'type' : 'password',
        'placeholder' : "Enter your new password"
        }))
    repeatpassword = forms.CharField(widget = forms.TextInput(attrs={
        'label' : "Confirm Password ",
        'class': "form-control",
        'id' : "floatingpasswordinput2",
        'type' : 'password',
        'placeholder' : "Confirm your password"
        }))
    class Meta:
        model=User
        fields = ('username', 'currentpassowrd', 'newrepeatpassword', 'repeatpassword')
    
    def __init__(self, *args, **kwargs):
        super(myUserCreationForm, self).__init__(*args, **kwargs)

class DocumentaryForm(forms.ModelForm):
    username = forms.CharField(widget = forms.TextInput(attrs={
        'label' : 'Username',
        'class': "form-control",
        'id' : "usernametextinput",
        'type' : 'text',
        'placeholder' : "Enter username"
        }))
    password1 = forms.CharField(widget = forms.TextInput(attrs={
        'class': "form-control",
        'id' : "floatingpasswordinput1",
        'type' : 'password',
        'placeholder' : "Enter your password"
        }))
    password2 = forms.CharField(widget = forms.TextInput(attrs={
        'label' : "Confirm Password ",
        'class': "form-control",
        'id' : "floatingpasswordinput2",
        'type' : 'password',
        'placeholder' : "Confirm your password"
        }))
    class Meta:
        fields = ('username', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super(DocumentaryForm, self).__init__(*args, **kwargs)


class DocumentForm(forms.Form):
    file = forms.FileField()