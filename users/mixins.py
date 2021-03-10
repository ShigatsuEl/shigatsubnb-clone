from django.shortcuts import redirect, reverse
from django.contrib.auth.mixins import UserPassesTestMixin


class LoggedOutOnlyView(UserPassesTestMixin):

    """ LoggedOutOnly View Definition """

    permission_denied_message = "Page not found"

    # test_func메서드의 return 값이 false라면 handle_no_permission메서드가 호출된다
    # 로그인 상태(인증완료)라면 false를 반환하고 handle_no_permission메서드에서 redirect합니다
    def test_func(self):
        return not self.request.user.is_authenticated

    def handle_no_permission(self):
        return redirect(reverse("core:home"))
