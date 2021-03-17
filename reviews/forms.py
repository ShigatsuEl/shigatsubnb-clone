from django import forms
from . import models


class CreateReviewForm(forms.ModelForm):

    """ CreateReview Form Definition """

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
        widgets = {
            "review": forms.Textarea(attrs={"class": "form-btn"}),
            "accurancy": forms.NumberInput(attrs={"class": "form-btn"}),
            "communication": forms.NumberInput(attrs={"class": "form-btn"}),
            "cleanliness": forms.NumberInput(attrs={"class": "form-btn"}),
            "location": forms.NumberInput(attrs={"class": "form-btn"}),
            "check_in": forms.NumberInput(attrs={"class": "form-btn"}),
            "value": forms.NumberInput(attrs={"class": "form-btn"}),
        }

    def save(self):
        review = super().save(commit=False)
        return review