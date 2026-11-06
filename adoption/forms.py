from django import forms
from .models import PetSubmission


class PetSubmissionForm(forms.ModelForm):

    class Meta:
        model = PetSubmission

        fields = [
            "pet_name",
            "breed",
            "age",
            "category",
            "gender",
            "vaccination",
            "stray",
            "relation",
            "address",
            "description",
            "image",
        ]

        widgets = {

            "pet_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Pet Name"
            }),

            "breed": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Breed"
            }),

            "age": forms.TextInput(attrs={
    "class": "form-control",
    "placeholder": "Example: 3 months or 2 years"
}),

            "category": forms.Select(attrs={
                "class": "form-control"
            }),

            "gender": forms.Select(attrs={
                "class": "form-control"
            }),

            "vaccination": forms.CheckboxInput(attrs={
                "class": "form-check-input"
            }),

            "stray": forms.Select(attrs={
                "class": "form-control"
            }),

            "relation": forms.Select(attrs={
                "class": "form-control"
            }),

            "address": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Address"
            }),

            "description": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "Describe the pet..."
            }),

            "image": forms.ClearableFileInput(attrs={
                "class": "form-control"
            }),
        }