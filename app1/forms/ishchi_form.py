from django import forms

from app1.models import Ishchi


class Ishchi_form(forms.ModelForm):
    class Meta:
        model = Ishchi
        fields = '__all__'
