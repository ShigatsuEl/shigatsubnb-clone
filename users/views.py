import os
from django.views.generic import FormView
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from . import forms
from . import models


class LoginView(FormView):

    """ Login View Definition """

    template_name = "users/login.html"
    form_class = forms.LoginForm
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            # A backend authenticated the credentials
            login(self.request, user)
        return super().form_valid(form)


def logout_view(request):
    logout(request)
    return redirect("core:home")


class SignUpView(FormView):

    """ SignUp View Deifinition """

    template_name = "users/singup.html"
    form_class = forms.SignUpForm
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        form.save()
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        user.verify_email()
        return super().form_valid(form)


def complete_verification(request, key):
    try:
        user = models.User.objects.get(email_secret=key)
        user.email_verified = True
        user.email_sercret = ""
        user.save()
        # to do: success message
    except models.User.DoesNotExist:
        # to do: error message
        raise
    return redirect(reverse("core:home"))


def github_login(request):
    client_id = os.environ.get("GITHUB_ID")
    redirect_uri = "http://127.0.0.1:8000/users/login/github/callback"
    return redirect(
        f"https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&scope=read:user"
    )


def github_callback(request):
    pass