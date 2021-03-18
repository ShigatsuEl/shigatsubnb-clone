import os
import requests
from django.http import HttpResponse
from django.contrib.auth.views import PasswordChangeView
from django.views.generic import FormView, DetailView, UpdateView
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.core.files.base import ContentFile
from . import forms
from . import models
from . import mixins


class LoginView(mixins.LoggedOutOnlyMixin, FormView):

    """ Login View Definition """

    template_name = "users/login.html"
    form_class = forms.LoginForm

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            # A backend authenticated the credentials
            login(self.request, user)
        return super().form_valid(form)

    # get_success_url메서드는 로그인 후 원래 가고자 했던 url로 redirect해줄 것이다
    def get_success_url(self):
        next_arg = self.request.GET.get("next")
        if next_arg is not None:
            return next_arg
        else:
            return reverse("core:home")


def logout_view(request):
    messages.info(
        request, f"{request.user.first_name + request.user.last_name} is logged out"
    )
    logout(request)
    return redirect("core:home")


class SignUpView(mixins.LoggedOutOnlyMixin, FormView):

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
                raise GithubException("Can't get authorization code")
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
                            raise GithubException(
                                f"You already have an account in a different way by {user.login_method}"
                            )
                    # DB에 user가 존재하지 않으면 Github을 통해 새 유저를 만들고 로그인하여 홈으로 리다이렉트한다
                    except models.User.DoesNotExist:
                        user = models.User.objects.create(
                            email=email,
                            first_name=name,
                            username=email,
                            bio=bio,
                            login_method=models.User.LOGIN_GITHUB,
                            email_verified=True,
                        )
                        user.set_unusable_password()
                        user.save()
                    login(request, user)
                    messages.success(
                        request, f"Welcome {user.first_name + user.last_name}"
                    )
                    return redirect(reverse("core:home"))
                else:
                    raise GithubException("Can't get your github profile")
        else:
            raise GithubException("Can't get authorization code")
    except GithubException as e:
        messages.error(request, e)
        return redirect(reverse("users:login"))


def kakao_login(request):
    # Kakao Login 클릭 시, Kakao authorize로 이동
    # Kakao authorize 페이지에서 모든 정보를 동의 후 callback url로 redirect
    REST_API_KEY = os.environ.get("KAKAO_KEY")
    REDIRECT_URI = "http://127.0.0.1:8000/users/login/kakao/callback"
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={REST_API_KEY}&redirect_uri={REDIRECT_URI}&response_type=code"
    )


class KakaoException(Exception):
    pass


def kakao_callback(request):
    try:
        # code를 통해 token으로 발급받는 과정
        code = request.GET.get("code")
        REST_API_KEY = os.environ.get("KAKAO_KEY")
        REDIRECT_URI = "http://127.0.0.1:8000/users/login/kakao/callback"
        token_request = requests.get(
            f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={REST_API_KEY}&redirect_uri={REDIRECT_URI}&code={code}"
        )
        token_json = token_request.json()
        error = token_json.get("error", None)
        # toekn을 받는데 실패하면 KakaoException 예외처리
        if error is not None:
            raise KakaoException("Can't get authorization code")
        access_token = token_json.get("access_token")
        profile_request = requests.get(
            "https://kapi.kakao.com/v2/user/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        profile_json = profile_request.json()
        email = profile_json.get("kakao_account", None).get("email")
        if email is None:
            raise KakaoException("Email was not given correctly.")
        nickname = profile_json.get("properties", None).get("nickname")
        profile_image = profile_json.get("properties", None).get("profile_image")
        # Kakao로 가입한 유저인지 확인 후 맞으면 로그인 처리, 다르면 KakaoException 예외처리
        try:
            user = models.User.objects.get(email=email)
            if user.login_method != models.User.LOGIN_KAKAO:
                raise KakaoException(
                    f"You already have an account in a different way by {user.login_method}"
                )
        # DB에 user가 존재하지 않으면 계정생성
        except models.User.DoesNotExist:
            user = models.User.objects.create(
                email=email,
                username=email,
                first_name=nickname,
                login_method=models.User.LOGIN_KAKAO,
                email_verified=True,
            )
            user.set_unusable_password()
            user.save()
            if profile_image is not None:
                # photo_request.content는 bullsheet file이다
                # ImageField인 avatar는 save메서드를 가지고 있는데 파일을 저장할 수 있게 해준다
                # content는 bullsheet file이기 때문에 Django에서 제공하는 ContentFile가 필요
                photo_request = requests.get(profile_image)
                user.avatar.save(
                    f"{nickname}-avatar", ContentFile(photo_request.content)
                )
        messages.success(request, f"Welcome {user.first_name + user.last_name}")
        login(request, user)
        return redirect(reverse("core:home"))
    except KakaoException as e:
        messages.error(request, e)
        return redirect(reverse("users:login"))


class UserProfileView(DetailView):

    """ UserProfile View Definition """

    model = models.User
    # DetailView는 문제점이 하나 있는데 로그인한 유저를 기억하지 못하고 뷰에서 찾았던 user object를 가리키게 된다
    # 때문에 profile을 가면 내 profile이 아닌 다른 사람의 profile을 보여주게 될 수도 있다
    # DetailView는 이것에 대한 해결책으로 context_object_name field를 바꿔 해결할 수 있다
    context_object_name = "user_obj"

    # get_context_data는 템플릿 안에 더 많은 context를 사용할 수 있게 해주는 method이다
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["hello"] = "Hello!"
        return context


class UpdateProfileView(mixins.LoggedInOnlyMixin, SuccessMessageMixin, UpdateView):

    """ UpdateProfile View Definition """

    model = models.User
    template_name = "users/update-profile.html"
    form_class = forms.UpdateProfileForm
    success_message = "Profile Updated"
    context_object_name = "user"

    def get_object(self, queryset=None):
        return self.request.user

    # form을 customize하기 위해서 2가지 방법이 있다
    # 1)form_class를 지정해 form을 만드는 방법
    # 2)UpdateView의 get_form메서드를 사용하는 방법
    """ 
    Ex)
    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields['birthdate'].widget.attrs = {'placeholder': 'Birthdate'}
    """


class UpdatePasswordView(
    mixins.LoggedInOnlyMixin,
    mixins.EmailLoginOnlyMixin,
    SuccessMessageMixin,
    PasswordChangeView,
):

    """ Update Password View """

    model = models.User
    template_name = "users/update-password.html"
    form_class = forms.UpdatePasswordForm
    success_message = "Password Updated"

    def get_context_data(self, **kwargs):
        user = self.request.user
        kwargs["user"] = user
        return super().get_context_data(**kwargs)

    def get_success_url(self):
        return self.request.user.get_absolute_url()


@login_required
def switch_hosting(request):

    # 세션에서 정보를 삭제하는 법
    # 1) del 키워드 사용 2) session pop을 사용
    try:
        del request.session["is_hosting"]
    except KeyError:
        # 세션에 정보를 추가하는 법
        request.session["is_hosting"] = True
    return redirect(reverse("core:home"))


def switch_language(request):

    lang = request.GET.get("lang", None)
    if lang is not None:
        pass
    return HttpResponse(status=200)