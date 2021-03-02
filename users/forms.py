from django import forms
from . import models


class LoginForm(forms.Form):

    """ Login Form Definition """

    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    # 지어낸 메서드가 아니며 어떠한 필드를 확인하고 싶다면 clean_(field)로 메서드를 설정한다
    # clean 메서드에서 어떤것도 return하지 않으면 기본적으로 field를 정리한다
    # clean 메서드에서 return하면 그것이 cleaned data가 된다
    def clean_email(self):
        email = self.cleaned_data.get("email")
        try:
            models.User.objects.get(username=email)
            return email
        except models.User.DoesNotExist:
            raise forms.ValidationError("User does not exist")

        # cleaned_data 메서드는 field를 정리한 결과물이다
        print(self.cleaned_data)

    def clean_password(self):
        print("clean password")
