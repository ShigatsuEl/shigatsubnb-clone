from django import forms


class AddCommentForm(forms.Form):

    """ AddComment Form Definition """

    message = forms.CharField(
        required=True,
        widget=forms.Textarea(
            attrs={"placeholder": "Add a Comment", "class": "form-btn"}
        ),
    )
