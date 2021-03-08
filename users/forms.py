from django import forms
from . import models


class LoginForm(forms.Form):

    """ Login Form Definition """

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email",
                "class": "form-btn rounded-t-lg",
            }
        ),
        label="",
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-btn rounded-b-lg mb-6",
            }
        ),
        label="",
    )

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


class SignUpForm(forms.ModelForm):

    """ SignUp Form Definition """

    class Meta:
        model = models.User
        fields = ("first_name", "last_name", "email")
        widgets = {
            "first_name": forms.TextInput(
                attrs={"placeholder": "First Name", "class": "form-btn rounded-t-lg"}
            ),
            "last_name": forms.TextInput(
                attrs={"placeholder": "Last Name", "class": "form-btn"}
            ),
            "email": forms.TextInput(
                attrs={"placeholder": "Email", "class": "form-btn"}
            ),
        }
        labels = {
            "first_name": "",
            "last_name": "",
            "email": "",
        }

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"placeholder": "Password", "class": "form-btn"}
        ),
        label="",
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Confirm Password",
                "class": "form-btn rounded-b-lg mb-6",
            }
        ),
        label="",
    )

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

    # save 메서드는 model을 통해 object를 생성하고 데이터베이스에 저장하는 역할을 한다
    def save(self, *args, **kwargs):
        # commit옵션을 False로 지정하면 object를 생성하지만 데이터베이스에 저장은 하지 않는다
        user = super().save(commit=False)
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        user.username = email
        user.set_password(password)
        user.save()
