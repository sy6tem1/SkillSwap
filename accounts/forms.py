from django import forms
from .models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("name", "description", "telegram", "photo")
        widgets = {
            "name": forms.TextInput(attrs={
                "class": "reg-field-input",
                "placeholder": "Имя"
            }),
            "description": forms.Textarea(attrs={
                "class": "reg-field-input textarea",
                "id": "descriptionField",
                "placeholder": "О себе",
                "style": "border-radius: 20px; line-height: 20px; "
            }),
            "telegram": forms.TextInput(attrs={
                "class": "reg-field-input",
                "placeholder": "@telegram"
            }),
        }

    def clean_description(self):
        description = self.cleaned_data.get("description", "")

        words = description.strip().split()
        if len(words) > 20:
            raise forms.ValidationError("Описание не может превышать 20 слов")

        return description

