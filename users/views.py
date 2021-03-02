from django.views import View
from django.shortcuts import render
from . import forms


class LoginView(View):

    """ Login View Definition """

    def get(self, request):
        form = forms.LoginForm(initial={"email": "shigatsu@gmail.com"})
        return render(request, "users/login.html", {"form": form})

    def post(self, request):
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            # cleaned_data는 clean메서드로 정리한 field들의 결과를 보여준다
            print(form.cleaned_data)
        return render(request, "users/login.html", {"form": form})
