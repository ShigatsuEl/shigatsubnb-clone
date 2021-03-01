from django import forms
from django_countries.fields import CountryField
from . import models


class SearchForm(forms.Form):

    city = forms.CharField(initial="Anywhere")
    country = CountryField(default="KR").formfield()
    # ModelChoiceField는 Select Option과 똑같은 Form 기능이다
    # ModelChoiceField는 Foreign Key에 해당한다
    # ModeleChoiceField는 인자로 QuerySet을 가진다
    room_type = forms.ModelChoiceField(
        required=False, empty_label="Any Kind", queryset=models.RoomType.objects.all()
    )
    price = forms.IntegerField(required=False)
    guests = forms.IntegerField(required=False)
    bedrooms = forms.IntegerField(required=False)
    beds = forms.IntegerField(required=False)
    baths = forms.IntegerField(required=False)
    instant_book = forms.BooleanField(required=False)
    superhost = forms.BooleanField(required=False)
    # ModelMultipleChoiceField는 Many to Many Field에 해당한다
    amenities = forms.ModelMultipleChoiceField(
        queryset=models.Amenity.objects.all(), widget=forms.CheckboxSelectMultiple
    )
    facilities = forms.ModelMultipleChoiceField(
        queryset=models.Facility.objects.all(), widget=forms.CheckboxSelectMultiple
    )
