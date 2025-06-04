from django import forms

from app_name.models import PrintClass


class PrintForm(forms.ModelForm):
    class Meta:
        model = PrintClass
        fields = ['name']