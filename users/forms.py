from django import forms
from . import models


class LoginForm(forms.Form):

    """ Login Form Definition """

    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    # 지어낸 메서드가 아니며 어떠한 필드를 확인하고 싶다면 clean_(field)로 메서드를 설정한다
    # clean 메서드에서 어떤것도 return하지 않으면 기본적으로 field를 정리한다
    # clean 메서드에서 return하면 그것이 cleaned data가 된다
    # clean 메서드를 썼으면 cleaned data를 꼭 사용하자
    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        try:
            user = models.User.objects.get(email=email)
            if user.check_password(password):
                return self.cleaned_data
            else:
                self.add_error("password", forms.ValidationError("Password is wrong"))
        except models.User.DoesNotExist:
            self.add_error("email", forms.ValidationError("User does not exist"))


class SignUpForm(forms.Form):

    """ SignUp Form Definition """

    first_name = forms.CharField(max_length=80)
    last_name = forms.CharField(max_length=80)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    password1 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        try:
            models.User.objects.get(email=email)
            raise forms.ValidationError("User already exists with that email")
        except models.User.DoesNotExist:
            return email

    # clean_password로 선언하면 작동하지 않을 것이다
    # Django는 순서대로 data를 clean하기 때문에 password를 clean하는 메서드엔 password1이 없다
    # 따라서 clean_password1으로 선언해야 password와 password1을 clean한 data를 확인할 수 있다
    def clean_password1(self):
        password = self.cleaned_data.get("password")
        password1 = self.cleaned_data.get("password1")

        if password != password1:
            raise forms.ValidationError("Password confirmation does not match")
        else:
            return password
