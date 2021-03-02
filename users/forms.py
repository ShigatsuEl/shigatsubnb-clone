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
