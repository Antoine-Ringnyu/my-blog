from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render
from django.urls import reverse

def dashboard(request):
    return render(request, "users/dashboard.html")

def sign_up(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse("blog:index"))
    else:
        form = UserCreationForm()
    return render(request, "registration/sign_up.html", {"form": form})