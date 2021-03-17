from django import forms
from . import models


class CreateReviewForm(forms.ModelForm):

    """ CreateReview Form Definition """

    # Form Validator 추가
    accurancy = forms.IntegerField(
        min_value=1, max_value=5, widget=forms.NumberInput(attrs={"class": "form-btn"})
    )
    communication = forms.IntegerField(
        min_value=1, max_value=5, widget=forms.NumberInput(attrs={"class": "form-btn"})
    )
    cleanliness = forms.IntegerField(
        min_value=1, max_value=5, widget=forms.NumberInput(attrs={"class": "form-btn"})
    )
    location = forms.IntegerField(
        min_value=1, max_value=5, widget=forms.NumberInput(attrs={"class": "form-btn"})
    )
    check_in = forms.IntegerField(
        min_value=1, max_value=5, widget=forms.NumberInput(attrs={"class": "form-btn"})
    )
    value = forms.IntegerField(
        min_value=1, max_value=5, widget=forms.NumberInput(attrs={"class": "form-btn"})
    )

    class Meta:
        model = models.Review
        fields = (
            "review",
            "accurancy",
            "communication",
            "cleanliness",
            "location",
            "check_in",
            "value",
        )
        widgets = {"review": forms.Textarea(attrs={"class": "form-btn"})}

    def save(self):
        review = super().save(commit=False)
        return review