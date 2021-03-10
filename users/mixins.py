from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import redirect, reverse
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin


# Log Out 유저만 통과하는 Mixin
class LoggedOutOnlyMixin(UserPassesTestMixin):

    """ LoggedOutOnly Mixin Definition """

    # test_func메서드의 return 값이 false라면 handle_no_permission메서드가 호출된다
    # 로그인 상태(인증완료)라면 false를 반환하고 handle_no_permission메서드에서 redirect합니다
    def test_func(self):
        return not self.request.user.is_authenticated

    def handle_no_permission(self):
        messages.error(self.request, "Can't go there")
        return redirect(reverse("core:home"))


# Log In 유저만 통과하는 Mixin
class LoggedInOnlyMixin(LoginRequiredMixin):

    """ LoggedInOnly Mixin Definition """

    login_url = reverse_lazy("users:login")


# Email 로그인 유저만 통과하는 Mixin
class EmailLoginOnlyMixin(UserPassesTestMixin):

    """ EmailLoginOnly Mixin Definition """

    def test_func(self):
        return self.request.user.login_method == "email"

    def handle_no_permission(self):
        messages.error(self.request, "Can't go there")
        return redirect(reverse("core:home"))
