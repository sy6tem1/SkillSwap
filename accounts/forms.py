from django import forms
from .models import Profile

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("name", "description", "telegram", "photo")

    def clean_description(self):
        description = self.cleaned_data.get("description", "")

        words = description.strip().split()
        if len(words) > 20:
            raise forms.ValidationError("Описание не может превышать 20 слов")

        return description
