import calendar
from django.utils import timezone


class Day:

    """ Day Definition """

    def __init__(self, number, month, year, past):
        self.number = number
        self.month = month
        self.year = year
        self.past = past

    def __str__(self):
        return str(self.number)


class Calendar(calendar.Calendar):

    """ Calendar Definition """

    def __init__(self, year, month):
        super().__init__(firstweekday=6)
        self.year = year
        self.month = month
        self.days = ("Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat")
        self.months = (
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December",
        )

    def get_days(self):
        weeks = self.monthdays2calendar(self.year, self.month)
        days = []
        for week in weeks:
            # tuple 안에 2개밖에 없기 때문에 day와 week_day로 나눌 수 있다
            # 자바스크립트로 비교하면 구조 분해할당을 한 것과 같다
            # _문자는 사용하지 않겠다는 의미를 나타낸다
            for day, _ in week:
                now = timezone.now()
                today = now.day
                month = now.month
                past = False
                if month == self.month:
                    if day <= today:
                        past = True
                new_day = Day(number=day, month=self.month, year=self.year, past=past)
                days.append(new_day)
        return days

    def get_month(self):
        return self.months[self.month - 1]