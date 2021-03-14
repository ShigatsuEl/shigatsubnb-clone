from django import forms
from django_countries.fields import CountryField
from . import models


# Djnago Template에서 Form을 만드는 대신 forms.py에서 Form을 간편하게 생성한다
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
        required=False,
        queryset=models.Amenity.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
    facilities = forms.ModelMultipleChoiceField(
        required=False,
        queryset=models.Facility.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )


class UpdateRoomForm(forms.ModelForm):

    """ UpdateRoom Form Definition """

    class Meta:

        model = models.Room
        fields = (
            "name",
            "description",
            "country",
            "city",
            "price",
            "address",
            "guests",
            "beds",
            "bedrooms",
            "baths",
            "check_in",
            "check_out",
            "instant_book",
            "room_type",
            "amenities",
            "facilities",
            "house_rules",
        )
        widgets = {
            "name": forms.TextInput(
                attrs={"placeholder": "Room Name", "class": "form-btn rounded-t-lg"}
            ),
            "description": forms.Textarea(attrs={"class": "form-btn"}),
            "country": forms.Select(attrs={"class": "form-btn"}),
            "city": forms.TextInput(attrs={"placeholder": "City", "class": "form-btn"}),
            "price": forms.NumberInput(attrs={"class": "form-btn"}),
            "address": forms.TextInput(attrs={"class": "form-btn"}),
            "guests": forms.NumberInput(attrs={"class": "form-btn"}),
            "beds": forms.NumberInput(attrs={"class": "form-btn"}),
            "bedrooms": forms.NumberInput(attrs={"class": "form-btn"}),
            "baths": forms.NumberInput(attrs={"class": "form-btn"}),
            "check_in": forms.TimeInput(
                attrs={"type": "time", "placeholder": "Check In", "class": "form-btn"}
            ),
            "check_out": forms.TimeInput(
                attrs={"type": "time", "placeholder": "Check Out", "class": "form-btn"}
            ),
            "instant_book": forms.CheckboxInput(attrs={"class": "border px-2 py-3"}),
            "room_type": forms.Select(attrs={"class": "form-btn"}),
            "amenities": forms.SelectMultiple(attrs={"class": "form-btn"}),
            "facilities": forms.SelectMultiple(attrs={"class": "form-btn"}),
            "house_rules": forms.SelectMultiple(
                attrs={"class": "form-btn rounded-b-lg"}
            ),
        }


class UpdatePhotoForm(forms.ModelForm):

    """ UpdatePhoto Form Definitiom """

    class Meta:

        model = models.Photo
        fields = (
            "file",
            "caption",
        )
        widgets = {
            "file": forms.FileInput(attrs={"class": "form-btn"}),
            "caption": forms.TextInput(
                attrs={
                    "placeholder": "Photo description",
                    "class": "form-btn",
                }
            ),
        }


class CreatePhotoForm(forms.ModelForm):

    """ UploadPhoto Form Definition """

    class Meta:

        model = models.Photo
        fields = (
            "file",
            "caption",
        )
        widgets = {
            "file": forms.FileInput(attrs={"class": "form-btn"}),
            "caption": forms.TextInput(
                attrs={
                    "placeholder": "Photo description",
                    "class": "form-btn",
                }
            ),
        }

    def save(self, pk, *args, **kwargs):
        # commit옵션을 False로 지정하면 object를 생성하지만 데이터베이스에 저장은 하지 않는다
        photo = super().save(commit=False)
        room = models.Room.objects.get(pk=pk)
        photo.room = room
        photo.save()


class CreateRoomForm(forms.ModelForm):

    """ CreateRoom Form Definitio """

    class Meta:

        model = models.Room
        fields = (
            "name",
            "description",
            "country",
            "city",
            "price",
            "address",
            "guests",
            "beds",
            "bedrooms",
            "baths",
            "check_in",
            "check_out",
            "instant_book",
            "room_type",
            "amenities",
            "facilities",
            "house_rules",
        )
        widgets = {
            "name": forms.TextInput(
                attrs={"placeholder": "Room Name", "class": "form-btn rounded-t-lg"}
            ),
            "description": forms.Textarea(attrs={"class": "form-btn"}),
            "country": forms.Select(attrs={"class": "form-btn"}),
            "city": forms.TextInput(attrs={"placeholder": "City", "class": "form-btn"}),
            "price": forms.NumberInput(attrs={"class": "form-btn"}),
            "address": forms.TextInput(attrs={"class": "form-btn"}),
            "guests": forms.NumberInput(attrs={"class": "form-btn"}),
            "beds": forms.NumberInput(attrs={"class": "form-btn"}),
            "bedrooms": forms.NumberInput(attrs={"class": "form-btn"}),
            "baths": forms.NumberInput(attrs={"class": "form-btn"}),
            "check_in": forms.TimeInput(
                attrs={"type": "time", "placeholder": "Check In", "class": "form-btn"}
            ),
            "check_out": forms.TimeInput(
                attrs={"type": "time", "placeholder": "Check Out", "class": "form-btn"}
            ),
            "instant_book": forms.CheckboxInput(attrs={"class": "border px-2 py-3"}),
            "room_type": forms.Select(attrs={"class": "form-btn"}),
            "amenities": forms.SelectMultiple(attrs={"class": "form-btn"}),
            "facilities": forms.SelectMultiple(attrs={"class": "form-btn"}),
            "house_rules": forms.SelectMultiple(
                attrs={"class": "form-btn rounded-b-lg"}
            ),
        }

    def save(self, *args, **kwargs):
        # commit옵션을 False로 지정하면 object를 생성하지만 데이터베이스에 저장은 하지 않는다
        room = super().save(commit=False)
        return room
