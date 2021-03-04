import os
import requests
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
    # Github Login을 클릭시 Github로 유저를 이동시키며 아래와 같은 정보가 필요하다
    client_id = os.environ.get("GITHUB_ID")
    redirect_uri = "http://127.0.0.1:8000/users/login/github/callback"
    return redirect(
        f"https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&scope=read:user"
    )


class GithubException(Exception):
    pass


def github_callback(request):
    try:
        # Github에서 user가 authorize 수락을 하게되면 Github은 다음과 같은 작업을 하고 user를 home으로 redirect한다
        # Github에서 authorize 수락 후 user에게 code를 발급하는데 이것은 access_token으로 바꿀 수 있는 역할을 한다
        client_id = os.environ.get("GITHUB_ID")
        client_secret = os.environ.get("GITHUB_SECRET")
        code = request.GET.get("code", None)
        # code가 존재한다면 정상적으로 authorize했다는 의미이다
        # code를 받아왔다면 code로부터 token을 만들수 있다
        # code는 10분 limit time이 존재하기 때문에 code가 없는 경우 home으로 redirect시킨다
        if code is not None:
            token_request = requests.post(
                f"https://github.com/login/oauth/access_token?client_id={client_id}&client_secret={client_secret}&code={code}",
                headers={"Accept": "application/json"},
            )
            token_json = token_request.json()
            error = token_json.get("error", None)
            # code가 limit time이 지나 만료된 code로 access_token을 얻으려 한다면 error가 발생
            if error is not None:
                raise GithubException()
            else:
                # ACCESS TOKEN을 얻는다면 이제 정상적으로 Github에게 API를 요청할 수 있다
                access_token = token_json.get("access_token")
                # ACCESS TOKEN을 가지고 Github에게 profile을 요청
                profile_request = requests.get(
                    "https://api.github.com/user",
                    headers={
                        "Authorization": f"token {access_token}",
                        "Accept": "application/json",
                    },
                )
                profile_json = profile_request.json()
                username = profile_json.get("login", None)
                # username이 없다는 것은 Github에서 user정보를 받아오지 못함을 의미
                if username is not None:
                    # Github에서 받아온 json에 name & email & bio가 None이면 아래와 같이 삼항처리
                    name = profile_json.get("name")
                    name = username if name is None else name
                    email = profile_json.get("email")
                    email = name if email is None else email
                    bio = profile_json.get("bio")
                    bio = "" if bio is None else bio
                    # Github으로 login을 시도할 때 user가 db에 존재한다면 로그인, 아니면 에러를 발생시킨다
                    try:
                        user = models.User.objects.get(email=email)
                        if user.login_method != models.User.LOGIN_GITHUB:
                            raise GithubException()
                    # DB에 user가 존재하지 않으면 Github을 통해 새 유저를 만들고 로그인하여 홈으로 리다이렉트한다
                    except models.User.DoesNotExist:
                        user = models.User.objects.create(
                            email=email,
                            first_name=name,
                            username=email,
                            bio=bio,
                            login_method=models.User.LOGIN_GITHUB,
                        )
                        user.set_unusable_password()
                        user.save()
                    login(request, user)
                    return redirect(reverse("core:home"))
                else:
                    raise GithubException()
        else:
            raise GithubException()
    except GithubException:
        # send error message
        return redirect(reverse("users:login"))
