from django import forms
from . import models


class SearchForm(forms.Form):

    city = forms.CharField(initial="Anywhere")
    price = forms.IntegerField(required=False)
    # ModelChiceField는 Select Option과 똑같은 Form 기능이다
    # ModeleChoiceField는 인자로 QuerySet을 가진다
    room_type = forms.ModelChoiceField(queryset=models.RoomType.objects.all())
