import json
from typing import List
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import PasswordResetForm
from django.contrib import messages
from UserApp.forms import myUserCreationForm
from . import models
from django.contrib.auth.decorators import login_required
def login_view(request):
    if request.user.is_authenticated:
        return redirect('default_view')
    if request.method == 'POST':
        data = ""
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponse(data)
        data="Invalid username or password"
        return HttpResponse(data)
    return render(request, 'login.html')# Create a login.html template for the login form

def logout_view(request):
    logout(request)
    return redirect('default_view')  # Replace 'home' with the name of your home view

def signup_view(request):
    if request.method == 'POST':
        form = myUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            user = models.User.objects.get(pk = models.User.objects.latest('date_joined').pk)
            models.UserInfo(user = user).save(force_insert=True)
            messages.success(request, 'Account created successfully. You can now log in.')
            return redirect('login')
    else:
        form = myUserCreationForm()
    return render(request, 'signup.html', {'form': form})  # Create a signup.html template for the signup form
@login_required
def password_reset_view(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            form.save(
                request=request,
                use_https=request.is_secure(),
                from_email='theunclefox@example.com',  # Set your email here
                email_template_name='password_reset_email.html',  # Create this template
                subject_template_name='password_reset_subject.txt',  # Create this template
            )
            pass
    else:
        form = PasswordResetForm()

    return render(request, 'password_reset.html', {'form': form})  # Create a password_reset.html template for the password reset form
def userprofile(request,iduser):
    userinfo = models.UserInfo.objects.filter(user__pk = iduser).first()
    list_userdocumentsection = models.UserDocumentSection.objects.filter(userdocumentary__user__id = iduser).all()
    list_userquiz = list()
    index=0
    for userdocumentsection in list_userdocumentsection:
        if len(list_userquiz) == 2:break
        userquiz = models.UserQuiz.objects.filter(userdocumentsection = userdocumentsection)
        for uq in userquiz:  
            if uq.isover:
                list_userquiz.append(uq)
                if len(list_userquiz) == 2:break
    if userinfo:
        return render(request, "profile.html",{"userinfo": userinfo,"userquiz":list_userquiz})
    return HttpResponse(request,"Người dùng không tồn tại")