from django.shortcuts import render, redirect

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("accounts:login")
    else:
        form = UserCreationForm()

    return render(request, "accounts/register.html", {"form": form})

def custom_logout(request):
    logout(request)
    messages.success(request, "You’ve been logged out successfully!")
    return redirect('/')
