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
