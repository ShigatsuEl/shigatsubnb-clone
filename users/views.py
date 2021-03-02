from django.views import View
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from . import forms


class LoginView(View):

    """ Login View Definition """

    def get(self, request):
        form = forms.LoginForm(initial={"email": "shigatsu@gmail.com"})
        return render(request, "users/login.html", {"form": form})

    def post(self, request):
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=email, password=password)
            if user is not None:
                # A backend authenticated the credentials
                login(request, user)
                return redirect(reverse("core:home"))
            else:
                # No backend authenticated the credentials
                pass
        return render(request, "users/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("core:home")
